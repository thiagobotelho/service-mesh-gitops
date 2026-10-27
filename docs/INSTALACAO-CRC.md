# Instalação no OpenShift Local

## 1. Conferir os pré-requisitos

Leia [REQUISITOS.md](REQUISITOS.md). Confira contexto, versão, capacidade e catálogo:

```bash
oc config current-context
oc whoami
oc get clusterversion
oc get nodes
oc adm top nodes
oc -n openshift-marketplace get packagemanifest servicemeshoperator3
```

Revise o canal e a versão dos manifests conforme a compatibilidade do OpenShift. No checkout de service-mesh-gitops, renderize as entradas Kustomize antes de aplicar:

```bash
kubectl kustomize operator/
kubectl kustomize overlays/desenvolvimento/
```

Se o namespace de aplicações já contiver recursos com os mesmos nomes, compare os manifests e planeje sua adoção ou migração. Não exclua o namespace para contornar conflitos de seletores. O script check-ownership.sh, no projeto mesh-apps-lab, identifica colisões de propriedade.

## 2. Cadastrar as Applications no Argo CD

No checkout de argocd-gitops:

```bash
oc apply -k optional/service-mesh
oc -n openshift-gitops get applications.argoproj.io
```

Esse diretório cadastra quatro Applications com sincronização manual: service-mesh-operator, service-mesh-control-plane, service-mesh-monitoring e mesh-apps-lab. Não instala os componentes até a sincronização. Não faz parte da stack base.

## 3. Executar o cenário sem Mesh

Selecione scenarios/01-baseline no Application mesh-apps-lab, revise o diff e sincronize. A base cria httpbin, sleep e sleep-denied, sem sidecars obrigatórios ou políticas. Aguarde os rollouts e execute verify-samples.sh.

Selecione scenarios/02-networkpolicy para exercitar L3/L4 e execute test-networkpolicy.sh. Retorne ao baseline com prune antes de testar o Mesh.

## 4. Instalar o Operator

Sincronize somente service-mesh-operator. A Subscription usa aprovação Manual. Inspecione o InstallPlan e aprove apenas o plano da versão escolhida; não aprove todos os planos do namespace compartilhado.

```bash
oc -n openshift-operators get subscription,installplan,csv
oc get crds | grep -E 'sailoperator|istio'
```

Aguarde CSV Succeeded e CRDs Established. Não crie outro OperatorGroup em openshift-operators.

## 5. Instalar o plano de controle

Sincronize service-mesh-control-plane. Esse estágio cria Istio, IstioCNI, namespaces e a tag de revisão. Aguarde condições saudáveis e execute, no projeto service-mesh-gitops:

```bash
bash scripts/verify-control-plane.sh
oc get istios,istiocnis,istiorevisions,istiorevisiontags
oc -n istio-system get pods
oc -n istio-cni get pods
```

Consulte a revisão real pela tag e confirme sua correspondência com a revisão ativa do Istio. Não derive o nome da revisão apenas da versão. O plano de controle e o CNI devem estar prontos antes da injeção.

## 6. Habilitar sidecar e políticas por fase

Alterne um cenário por vez no mesmo Application mesh-apps-lab e sincronize com prune revisado:

| Caminho | Objetivo |
|---|---|
| scenarios/03-mesh | injetar proxies e conferir conectividade |
| scenarios/04-mtls-strict | exigir mTLS e testar cliente sem proxy |
| scenarios/05-authorization | permitir somente a identidade, método e caminho autorizados |
| scenarios/06-defense-in-depth | combinar NetworkPolicy e controles do Mesh |

As anotações do template disparam novos pods. Confirme o container istio-proxy pronto em httpbin, sleep e sleep-denied. Não crie Applications concorrentes para cenários distintos: prune retira as políticas e os clientes exclusivos da fase anterior.

## 7. Habilitar observabilidade

Sincronize service-mesh-monitoring após criar os namespaces e verificar as CRDs do monitoramento. Confira os seletores do Prometheus. O dashboard é provisionado pelo overlay desenvolvimento do projeto grafana-gitops; não aplique em paralelo os assets de referência.

Gere tráfego limitado, verifique as séries e abra o Grafana seguindo [GRAFANA.md](GRAFANA.md). Consulte [EXERCICIOS.md](EXERCICIOS.md) para os testes e [ROLLBACK-E-CLEANUP.md](ROLLBACK-E-CLEANUP.md) para desfazer a instalação.

## Tracing opcional

optional/tracing é uma alternativa à fonte do plano de controle, reutilizando o Collector existente. Substitua o caminho do mesmo Application, sem criar um segundo proprietário do Istio. Confira serviço OTLP, conectividade e spans no Tempo antes de depender do drilldown. Kiali, Vault e PKI externa são módulos de evolução separados.
