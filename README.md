# service-mesh-gitops

Infraestrutura OpenShift Service Mesh 3 em Sidecar, com Istio CNI e integração opcional com a observabilidade já existente.

Laboratório pessoal para OpenShift Local. **Preparado e validado estaticamente; implantação e homologação funcional pendentes.** No CRC auditado existem exercícios anteriores em mesh-lab; a adoção precisa de revisão antes de sincronizar. Não executar contra cluster corporativo.

## Início rápido

1. Ler [instalação](docs/INSTALACAO-CRC.md) e [inventário](docs/INVENTARIO.md).
2. Conferir contexto e recursos com `bash scripts/preflight.sh` (somente leitura).
3. Validar fontes com `bash scripts/validate.sh` (kubectl, Python/PyYAML/jsonschema, Kubeconform 0.7.0 e ShellCheck).
4. Após autorização, seguir os gates do Operator, plano de controle e cenários no Argo CD. Nada é ativado automaticamente na stack existente.

## Entradas Kustomize

| Caminho | Uso |
|---|---|
| operator/ | Subscription 3.4.3, canal stable-3.4, aprovação Manual |
| overlays/desenvolvimento/ | Istio v1.30.5, IstioCNI, tag mesh-crc e namespaces |
| monitoring/ | PodMonitor/ServiceMonitor RHOBS para Prometheus existente |
| optional/tracing/ | alternativa ao overlay principal, com provider OTLP existente |
| assets/grafana/ | CRs de referência; integração proposta no grafana-gitops |

Instalar em fases. O tracing é **alternativa** à mesma fonte do plano de controle, nunca um segundo Application concorrente para o mesmo Istio. Os assets Grafana não são parte da base e não devem ter dois proprietários. Sem Kiali, Vault, Prometheus/Grafana/Tempo adicionais. [Procedência dos schemas e versões](docs/PROCEDENCIA.md).

## Guias

- [Arquitetura e Mermaid](docs/ARQUITETURA.md)
- [Primeiro teste manual](docs/01-primeiro-teste.md)
- [Exercícios e resultados esperados](docs/EXERCICIOS.md)
- [NetworkPolicy e Service Mesh](docs/NETWORKPOLICY-VS-SERVICE-MESH.md)
- [Métricas, PromQL e Grafana](docs/GRAFANA.md)
- [Diagnóstico](docs/TROUBLESHOOTING.md)
- [Rollback e limpeza](docs/ROLLBACK-E-CLEANUP.md)
- [Matriz de validação](docs/MATRIZ-VALIDACAO.md)
- [Relatório final](docs/RELATORIO-FINAL.md)
- [Evolução de PKI](docs/ROADMAP-VAULT.md)

Documentação operacional em Markdown/português. YAML, shell, JSON e testes mantêm extensões funcionais. Nenhuma credencial deve ser inserida nos exemplos, relatórios ou commits. Licença Apache 2.0, com avisos originais preservados.
