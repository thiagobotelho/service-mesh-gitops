# Operação do Service Mesh

## Selecionar cenário

Use um único Application mesh-apps-lab para todos os cenários. Modifique spec.source.path e sincronize com prune revisado:

```bash
oc -n openshift-gitops patch application mesh-apps-lab --type=merge \
  -p '{"spec":{"source":{"path":"scenarios/04-mtls-strict"}}}'
```

Na interface do Argo CD, revise o diff e selecione Sync com prune. Aguarde o fim da operação e os rollouts antes de testar. [Exercícios](EXERCICIOS.md).

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

Retorne ao cenário sem Mesh e confirme ausência de proxies. Retire as Applications sem exclusão em cascata e execute somente os procedimentos de [limpeza](ROLLBACK-E-CLEANUP.md). Não remova CNI compartilhado, CRDs, namespace ou plataformas de observabilidade por um cleanup genérico.
