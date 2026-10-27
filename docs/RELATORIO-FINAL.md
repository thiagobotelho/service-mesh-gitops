# Relatório da preparação do laboratório

## Entrega

Implementação de infraestrutura Service Mesh 3 em Sidecar e seis cenários com exemplos oficiais httpbin/sleep. Não foram criadas APIs novas nem duplicados Prometheus/Grafana/Tempo. Documentação operacional, guias, arquitetura, exercícios, matriz e backlog em Markdown/português. Sem mudanças de autenticação.

Fontes novas destinadas a:

- [service-mesh-gitops](https://github.com/thiagobotelho/service-mesh-gitops)
- [mesh-apps-lab](https://github.com/thiagobotelho/mesh-apps-lab)

Os dois repositórios pessoais foram criados públicos, com conteúdo sintético revisado para segredos. Não houve alteração de visibilidade do plugin privado.

| Projeto | Commit da implementação inicial | CI real concluído |
|---|---|---|
| mesh-apps-lab | [cbb3d2f](https://github.com/thiagobotelho/mesh-apps-lab/commit/cbb3d2f847c22f694bdfdbe399db54dfd56616e4) | [PASS](https://github.com/thiagobotelho/mesh-apps-lab/actions/runs/40428004454) |
| service-mesh-gitops | [4e5c13f](https://github.com/thiagobotelho/service-mesh-gitops/commit/4e5c13f7358d9dd6ded17109bf99eb7caec1f91d) | [PASS](https://github.com/thiagobotelho/service-mesh-gitops/actions/runs/40428019704) |

Os 111 arquivos iniciais foram relidos pela árvore Git e comparados com hashes de blobs e modos locais, sem divergências. Esta atualização documental também reforça as verificações de STRICT/L7 na fase combinada e da tag saudável ligada à revisão ativa. Seu CI deve ser conferido no histórico de Actions do commit correspondente; a tabela acima identifica exatamente os primeiros commits testados, sem atribuir seus resultados a versões posteriores.

Validação local: 18 entradas Kustomize novas, schemas Kubernetes 1.35 em modo strict, schemas Sail/Grafana/RHOBS/OLM e políticas Istio, ShellCheck, YAML/JSON, contratos de erro e bloqueio de contexto divergente. As sete propostas existentes passaram em 39 verificações de patch/render. A API do Prometheus aceitou as 12 consultas do dashboard, mas sem séries de tráfego Istio. absent() retornou a sentinela de ausência; não se trata de dados de requisição.

Não foram criados PRs nesses dois repositórios novos: as publicações iniciais foram feitas diretamente em seus históricos recém-criados, com mensagens em português. Nenhuma branch padrão preexistente foi alterada.

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
