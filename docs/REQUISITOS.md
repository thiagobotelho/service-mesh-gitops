# Requisitos e configuração

- OpenShift Local operacional e acesso administrativo para instalar Operators e Istio CNI.
- Rede compatível com NetworkPolicy, como OVN-Kubernetes.
- Argo CD/OpenShift GitOps instalado e autorizado a gerenciar os namespaces e recursos do Mesh.
- Ferramentas oc, kubectl com Kustomize, Bash e curl. Para validação estática: Python 3, PyYAML, jsonschema, ShellCheck e Kubeconform.
- Acesso aos registries e ao catálogo configurados nos manifests. Recursos de CPU/memória disponíveis para o plano de controle, CNI e proxies.

## Parâmetros dos manifests

| Parâmetro | Local | Como adaptar |
|---|---|---|
| Canal/CSV do Operator | service-mesh-gitops/operator/subscription.yaml | escolher versão compatível com o OpenShift e disponível no catálogo |
| Versão de Istio/CNI | service-mesh-gitops/base | manter versões compatíveis entre si e com o Operator |
| Namespace das aplicações | mesh-apps-lab/base | ajustar também políticas, monitores e principal SPIFFE |
| Discovery selector e tag | service-mesh-gitops/base | manter coerência com labels de namespace e injeção |
| Trust domain | Istio meshConfig.trustDomain | atualizar os principals das AuthorizationPolicies ao alterar |
| Monitoramento | service-mesh-gitops/monitoring | adaptar API group, labels e namespace do Prometheus |
| Grafana | grafana-gitops/overlays/desenvolvimento | conferir instanceSelector e UID do datasource |

Consulte a [procedência e referências](PROCEDENCIA.md) e a matriz de compatibilidade do fabricante antes de selecionar versões. Versões fixadas nos manifests são configuração do projeto; confirme sua disponibilidade e ciclo de vida antes de instalar.

Os scripts operacionais de conveniência têm proteção para o contexto crc-admin e API padrão do OpenShift Local, exigindo nó único crc. Para outro ambiente, adapte o alvo e revise as proteções antes de executar. Não reutilize automaticamente esses scripts em clusters compartilhados.
