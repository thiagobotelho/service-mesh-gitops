# Operação do Service Mesh

## Separar infraestrutura e exercícios

No Argo CD, sincronize a Application `service-mesh`, que reúne Operator, CNI, plano de controle, tag e monitores. As sync waves respeitam a ordem de dependências; acompanhe a saúde de cada etapa.

As APIs de teste são operadas manualmente no repositório mesh-apps-lab. Para alternar cenários, use oc apply -k e remova apenas os recursos exclusivos da fase anterior conforme [APLICACAO-MANUAL.md](APLICACAO-MANUAL.md).

## Consultar saúde

```bash
oc -n openshift-gitops get applications.argoproj.io
oc get istios,istiocnis,istiorevisions,istiorevisiontags
oc -n mesh-lab get deployments,pods,services,networkpolicies
oc -n mesh-lab get peerauthentications,authorizationpolicies
```

O status Synced representa convergência declarativa. Verifique também readiness dos pods, requisições da aplicação e telemetria para avaliar o funcionamento.

## Gerar tráfego de estudo

No checkout de mesh-apps-lab:

```bash
bash scripts/generate-traffic.sh 60 2
```

O script limita duração e taxa; não use carga ilimitada em OpenShift Local. Ajuste a janela temporal do Grafana para acompanhar as amostras.

## Atualizar versões

Revise compatibilidade e notas de versão. Atualize Subscription, versão Istio/CNI e imagens em conjunto quando necessário. Preserve aprovação Manual de InstallPlans. Inspecione a revisão ativa, tag, webhooks e rollouts antes de remover revisões antigas.

## Desinstalar

Retorne ao cenário sem Mesh e confirme ausência de proxies. Retire a Application sem exclusão em cascata e execute somente os procedimentos de [limpeza](ROLLBACK-E-CLEANUP.md). Não remova CNI compartilhado, CRDs, namespace ou plataformas de observabilidade por um cleanup genérico.
