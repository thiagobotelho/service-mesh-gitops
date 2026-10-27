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

## 2. Cadastrar a Application no Argo CD

No checkout de argocd-gitops:

```bash
oc apply -k optional/service-mesh
oc -n openshift-gitops get applications.argoproj.io
```

Esse diretório cadastra a Application `service-mesh`, com sincronização manual, reunindo Operator, CNI, plano de controle, tag e monitores em etapas ordenadas por sync waves. As APIs de teste ficam fora do Argo CD. Os componentes são instalados durante a sincronização. Configure previamente as verificações de saúde Sail de argocd-gitops/base/argocd.yaml e confira as CRDs de monitoramento. Não faz parte da stack base.

## 3. Preparar os exercícios manuais

No repositório mesh-apps-lab, revise os recursos existentes e siga o [guia manual](APLICACAO-MANUAL.md). Para o baseline sem Mesh, aplique scenarios/01-baseline com oc e execute verify-samples.sh. O Argo gerencia somente a infraestrutura; não cria, adota ou reinicia as APIs dos exercícios.

## 4. Instalar o Operator

Sincronize `service-mesh`. A etapa da Subscription precede os recursos Sail; acompanhe sua saúde no Argo CD. A Subscription usa aprovação Manual. Inspecione o InstallPlan e aprove apenas o plano da versão escolhida; não aprove todos os planos do namespace compartilhado.

```bash
oc -n openshift-operators get subscription,installplan,csv
oc get crds | grep -E 'sailoperator|istio'
```

Na primeira instalação, a sincronização aguarda aprovação do InstallPlan; após aprová-lo, aguarde CSV Succeeded e CRDs Established. A opção SkipDryRunOnMissingResource dos recursos Sail não substitui esse requisito. Não crie outro OperatorGroup em openshift-operators.

## 5. Instalar o plano de controle

Após a instalação do Operator, a mesma sincronização prossegue com IstioCNI, Istio e a tag de revisão. Os namespaces de infraestrutura são criados na primeira wave. Aguarde condições saudáveis e execute, no projeto service-mesh-gitops:

```bash
bash scripts/verify-control-plane.sh
oc get istios,istiocnis,istiorevisions,istiorevisiontags
oc -n istio-system get pods
oc -n istio-cni get pods
```

Consulte a revisão real pela tag e confirme sua correspondência com a revisão ativa do Istio. Não derive o nome da revisão apenas da versão. O plano de controle e o CNI devem estar prontos antes da injeção.

## 6. Habilitar sidecar e políticas por fase

No checkout de mesh-apps-lab, aplique um cenário por vez com oc apply -k. Remova explicitamente os recursos exclusivos da fase anterior, conforme [APLICACAO-MANUAL.md](APLICACAO-MANUAL.md):

| Caminho | Objetivo |
|---|---|
| scenarios/03-mesh | injetar proxies e conferir conectividade |
| scenarios/04-mtls-strict | exigir mTLS e testar cliente sem proxy |
| scenarios/05-authorization | permitir somente a identidade, método e caminho autorizados |
| scenarios/06-defense-in-depth | combinar NetworkPolicy e controles do Mesh |

As anotações do template disparam novos pods. Confirme o container istio-proxy pronto em httpbin, sleep e sleep-denied. Não cadastre as APIs no Argo CD. Como oc apply não executa prune, retire manualmente as políticas e os clientes exclusivos da fase anterior.

## 7. Habilitar observabilidade

Os monitores integram a última wave da Application `service-mesh`. As CRDs de monitoramento devem estar instaladas antes da sincronização. Confira os seletores do Prometheus. O dashboard é provisionado pelo overlay desenvolvimento do projeto grafana-gitops; não aplique em paralelo os assets de referência.

Gere tráfego limitado, verifique as séries e abra o Grafana seguindo [GRAFANA.md](GRAFANA.md). Consulte [EXERCICIOS.md](EXERCICIOS.md) para os testes e [ROLLBACK-E-CLEANUP.md](ROLLBACK-E-CLEANUP.md) para desfazer a instalação.

## Tracing opcional

optional/tracing é uma alternativa à fonte do plano de controle, reutilizando o Collector existente. Substitua o caminho da mesma Application por optional/tracing, que inclui toda a infraestrutura, sem criar um segundo proprietário do Istio. Confira serviço OTLP, conectividade e spans no Tempo antes de depender do drilldown. Kiali, Vault e PKI externa são módulos de evolução separados.
