# Instalação no CRC

## Estado e pré-requisitos

Em 26/10/2026 foram consultados, somente em leitura, OpenShift 4.22.1, OVN-Kubernetes, RHCOS 9.8, catálogo `stable-3.4` com `servicemeshoperator3.v3.4.3` e exemplo de Istio/CNI `v1.30.5`. A política Red Hat lista OCP 4.20/4.21/4.22 para a linha 3.4. Isso verifica a escolha documental; não certifica suporte comercial do CRC nem comprova instalação.

O nó tinha aproximadamente 25.747 MiB de memória em uso (64%) e CPU 5%. Refaça a medição antes de instalar. `mesh-lab` já contém `httpbin`, `sleep` e `intruso` criados previamente, sem propriedade deste laboratório. **A instalação está bloqueada até revisar a adoção ou migrar esses exercícios. Não apagar o namespace para resolver o conflito.**

Ferramentas: `oc`, `kubectl` com Kustomize, Bash, curl, Python 3. Para validação estática: ShellCheck, Kubeconform 0.7.0, PyYAML e jsonschema; o CI instala versões explícitas. `istioctl` compatível é opcional para inspeção adicional. A consulta ao cluster usa `oc` disponível no host, sem presumir conectores de diagnóstico.

```bash
# Executar nas fontes clonadas; comandos abaixo são orientações, não evidência de execução.
bash scripts/preflight.sh
```

Todos os scripts operacionais fixam `--context=crc-admin` e `--server=https://api.crc.testing:6443`, verificam o servidor do contexto e exigem o único nó `crc`. Nenhum comando modifica o contexto global. Não reutilizar em ambiente corporativo.

## Etapas de implantação, após autorização

1. Revisar `docs/PROCEDENCIA.md`, versões, recursos e colisões. Executar `mesh-apps-lab/scripts/check-ownership.sh`; neste CRC a saída esperada atualmente é `BLOCKED` devido aos objetos anteriores.
2. Revisar e aprovar a adoção de `httpbin`/`sleep`: comparar `oc get deployment,service,serviceaccount ... -o yaml` em armazenamento local protegido e o render; não versionar dumps contendo dados de credenciais. `intruso` permanece fora do gerenciamento. Nenhuma adoção foi executada nesta entrega.
3. Iniciar pelo cenário `01-baseline` no único Application `mesh-apps-lab`. Sem sidecar e sem políticas, executar `verify-samples.sh` e registrar os dois HTTP 200.
4. Selecionar `02-networkpolicy`, sincronizar com prune e testar; voltar ao baseline para restaurar conectividade.
5. Criar apenas a Application opcional do Operator, sem sync automático. Sincronizar `service-mesh-gitops/operator`. Inspecionar Subscription e InstallPlan em `openshift-operators` e aprovar **somente o plano que instala a versão revisada**. A aprovação é Manual; não aprovar todos os planos do namespace compartilhado.
6. Aguardar CSV `Succeeded` e CRDs `Established`. Sincronizar o plano de controle `overlays/desenvolvimento` e executar `service-mesh-gitops/scripts/verify-control-plane.sh`. Confirmar CNI, Istio, tag saudável e revisão real antes de avançar. Não aplicar um OperatorGroup adicional no namespace compartilhado.
7. Selecionar os cenários `03-mesh`, `04-mtls-strict`, `05-authorization`, `06-defense-in-depth`, um de cada vez. A mudança de anotação no template cria novos pods. Aguardar rollout e verificar `istio-proxy` pronto em cada pod.
8. Instalar `monitoring/` somente após existir `mesh-lab`. Publicar a proposta do dashboard em `grafana-gitops` após revisão e autorização. Gerar tráfego pequeno e executar `verify-observability.sh`.

## Troca segura de cenário pelo Argo CD

As Applications opcionais estão versionadas em `argocd-gitops/optional/service-mesh/`, fora do App-of-Apps. Não há sincronização automática. O mesmo Application `mesh-apps-lab` troca apenas `spec.source.path`.

```bash
# Exemplo operacional esperado, ainda não executado.
oc --context=crc-admin --server=https://api.crc.testing:6443 -n openshift-gitops \
  patch application mesh-apps-lab --type=merge \
  -p '{"spec":{"source":{"path":"scenarios/04-mtls-strict"}}}'
# Pela UI do Argo CD, revisar o diff e sincronizar com PRUNE habilitado.
```

`prune` remove a NetworkPolicy anterior ao entrar na fase de mTLS e remove `sleep-plain` ao avançar para autorização. Sem prune, políticas antigas podem mascarar resultados. Nunca criar seis Applications para o mesmo namespace nem usar `oc apply -k` sequencial sem remover os objetos exclusivos do cenário anterior. Sync waves não substituem os gates de readiness entre Applications.

## Versões e escopo

`startingCSV` fixa o ponto inicial, mas não congela permanentemente o catálogo. O Approval Manual controla novos InstallPlans. Istio e CNI fixam `v1.30.5`; a revisão final é determinada pelo Operator. Sidecar é o modo escolhido; ambient/ZTunnel, Kiali, gateways, SPIRE e PKI externa não são instalados. Não se depende de recursos Technology Preview neste escopo. Integrações opcionais não foram homologadas.
