#!/usr/bin/env python3
"""Valida artefatos locais; não acessa o cluster."""
import json,pathlib,subprocess,sys,re,hashlib
import yaml
root=pathlib.Path(__file__).resolve().parents[1]
def build(p):
 return [d for d in yaml.safe_load_all(subprocess.check_output(['kubectl','kustomize',str(p)],text=True)) if d]
def require(ok,msg):
 if not ok:raise AssertionError(msg)
import jsonschema
builds={}
for k in sorted(root.rglob('kustomization.yaml')):
 ds=build(k.parent);keys=[(d['apiVersion'],d['kind'],d['metadata'].get('namespace'),d['metadata']['name']) for d in ds]
 require(len(keys)==len(set(keys)),f'recursos duplicados: {k}')
 builds[str(k.parent.relative_to(root))]=ds
 for d in ds:
  schema=root/'tests/schemas'/f'{d["kind"]}.json'
  if schema.exists():jsonschema.validate(d,json.loads(schema.read_text()))
for p in root.rglob('*.yaml'):
 list(yaml.safe_load_all(p.read_text()))
for p in root.rglob('*.json'):json.loads(p.read_text())
for p in root.rglob('*.md'):
 for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
  if '://' in dest or dest.startswith('#'):continue
  dest=dest.split('#')[0]
  require((p.parent/dest).exists(),f'link local quebrado: {p} → {dest}')
if (root/'scenarios').exists():
 for phase,ds in builds.items():
  if not phase.startswith('scenarios/'):continue
  deps={d['metadata']['name']:d for d in ds if d['kind']=='Deployment'}
  for name in ['httpbin','sleep','sleep-denied']:
   d=deps[name];tpl=d['spec']['template'];s=d['spec']['selector']['matchLabels']
   require(all(tpl['metadata']['labels'].get(k)==v for k,v in s.items()),'selector não coincide com template')
   require(tpl['spec']['serviceAccountName']==name,'identidade de cliente colide')
   svc=next(d for d in ds if d['kind']=='Service' and d['metadata']['name']==name)
   require(svc['spec']['selector']['app']==name,'Service seleciona cliente errado')
   require('@sha256:' in tpl['spec']['containers'][0]['image'],'imagem sem digest')
   require(tpl['spec']['containers'][0]['securityContext']['capabilities']['drop']==['ALL'],'capacidade excessiva')
   injected=tpl['metadata']['annotations']['sidecar.istio.io/inject']
   require(injected==('false' if phase<'scenarios/03' else 'true'),'injeção na fase incorreta')
  net=[d for d in ds if d['kind']=='NetworkPolicy'];auth=[d for d in ds if d['kind']=='AuthorizationPolicy'];mtls=[d for d in ds if d['kind']=='PeerAuthentication']
  require(bool(net)==(phase.endswith('02-networkpolicy') or phase.endswith('06-defense-in-depth')),'NetworkPolicy mascara outra fase')
  require(bool(auth)==(phase.endswith('05-authorization') or phase.endswith('06-defense-in-depth')),'L7 na fase incorreta')
  require(bool(mtls)==(phase>='scenarios/04'),'mTLS na fase incorreta')
  for d in net:
   for rule in d['spec']['ingress']:
    require(rule['ports'][0]['port'] in [8080,15090],'porta de serviço usada em lugar da porta de container')
  for d in auth:
   rule=d['spec']['rules'][0]
   require(rule['from'][0]['source']['principals']==['cluster.local/ns/mesh-lab/sa/sleep'],'principal amplo')
   require(rule['to'][0]['operation']=={'methods':['GET'],'paths':['/get']},'permissão L7 ampla')
  if phase.endswith('04-mtls-strict'):
   require(deps['sleep-plain']['spec']['template']['metadata']['annotations']['sidecar.istio.io/inject']=='false','cliente negativo recebeu proxy')
 # Originais vendorizados não podem ser alterados silenciosamente.
 for name,expected in json.loads((root/'tests/vendor-sha256.json').read_text()).items():
  require(hashlib.sha256((root/'vendor'/name).read_bytes()).hexdigest()==expected,'sample original modificado')
else:
 import jsonschema
 # CRDs contêm extensões Kubernetes. JSON Schema valida tipos/valores; validação de admissão segue pendente.
 for ds in builds.values():
  for d in ds:
   if d['apiVersion'] in ['sailoperator.io/v1','monitoring.rhobs/v1','grafana.integreatly.org/v1beta1']:
    schema=json.loads((root/'tests/schemas'/f'{d["kind"]}.json').read_text());jsonschema.validate(d,schema)
 control=builds['base']
 tag=next(d for d in control if d['kind']=='IstioRevisionTag')
 istio=next(d for d in control if d['kind']=='Istio')
 require(tag['metadata']['name']!=istio['metadata']['name'],'tag colide com a revisão InPlace')
 require(tag['spec']['targetRef']=={'kind':'Istio','name':istio['metadata']['name']},'tag aponta para outro Istio')
 monitors=builds['monitoring']
 require(all(d['metadata'].get('namespace')=='istio-system' for d in monitors),'monitores fora da infraestrutura')
 require(next(d for d in monitors if d['kind']=='PodMonitor')['spec']['namespaceSelector']['matchNames']==['mesh-lab'],'namespace de coleta alterado')
 require(next(d for d in monitors if d['kind']=='ServiceMonitor')['spec']['selector']['matchExpressions']==[{'key':'istio.io/tag','operator':'DoesNotExist'}],'aliases de tag duplicam o scrape de Istiod')
 dash=json.loads((root/'assets/dashboard-service-mesh.json').read_text())
 require(dash['title']=='OpenShift Service Mesh — CRC Lab','título do dashboard')
 targets=[t['expr'] for p in dash['panels'] for t in p['targets']]
 for q in targets:
  if 'istio_request' in q:require('reporter="destination"' in q,'contagem dupla de métricas')
 for p in dash['panels']:
  if p['title'].startswith('Latência'):require(p['fieldConfig']['defaults']['unit']=='ms','unidade incoerente')
 embedded=next(d for d in builds['assets/grafana'] if d['kind']=='GrafanaDashboard')
 require(json.loads(embedded['spec']['json'])==dash,'dashboard JSON e CR divergentes')
print(f'PASS: {len(builds)} entradas Kustomize, YAML/JSON, links e contratos semânticos')
