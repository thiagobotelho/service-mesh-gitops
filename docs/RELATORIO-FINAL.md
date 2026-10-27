# Relatório da preparação do laboratório

## Entrega

Implementação de infraestrutura Service Mesh 3 em Sidecar e seis cenários com exemplos oficiais httpbin/sleep. Não foram criadas APIs novas nem duplicados Prometheus/Grafana/Tempo. Documentação operacional, guias, arquitetura, exercícios, matriz e backlog em Markdown/português. Sem mudanças de autenticação.

Fontes novas destinadas a:

- [service-mesh-gitops](https://github.com/thiagobotelho/service-mesh-gitops)
- [mesh-apps-lab](https://github.com/thiagobotelho/mesh-apps-lab)

A publicação e os commits efetivos serão registrados após a execução remota; os links de destino não constituem, isoladamente, evidência de publicação.

## Integrações propostas

Sete diffs locais: Applications opcionais no argocd-gitops; pasta/dashboard no grafana-gitops; orientações de coleta RHOBS em prometheus-gitops; tracing opcional em opentelemetry-gitops e tempo-gitops; distinção L3/L4 no network-observability-gitops; referência opcional no openshift-local-installer. Nenhum commit, branch remoto ou PR nos projetos existentes nesta etapa. Branch proposta para a revisão: laboratorio/service-mesh-crc. Os HEADs auditados estão em INVENTARIO.md; revalidar antes de gravar.

client-ip-api-openshift permanece sem alterações: finalidade distinta. Conteúdo do repositório privado de estudos não é republicado.

## Validação e pendências

Consultar [matriz](MATRIZ-VALIDACAO.md). A validação estática é separada da funcional. Não foram aplicados manifestos nem instalados Operators no CRC. Não há evidência de 200/403/mTLS/métricas reais deste novo laboratório. Há colisões nos objetos httpbin/sleep anteriores em mesh-lab, que precisam de revisão de adoção. Nenhuma alteração nesses recursos foi executada.

## Próxima execução, após autorização

```bash
# Fontes clonadas do mesh-apps-lab:
bash scripts/preflight.sh
bash scripts/check-ownership.sh
# Resolver o BLOCKED de adoção por revisão do diff, sem excluir os exercícios.
# Depois: seguir docs/INSTALACAO-CRC.md e sincronizar somente a fase revisada.
```

Aprovar gravação dos diffs existentes e abertura dos PRs como etapas distintas. Instalação no CRC exige autorização própria e nova confirmação do contexto. Não realizar merge automaticamente.
