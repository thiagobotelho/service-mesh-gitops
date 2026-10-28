# service-mesh-gitops

Infraestrutura OpenShift Service Mesh 3 em Sidecar, com Istio CNI e integração opcional com a observabilidade já existente.

Exemplos e infraestrutura declarativos para estudar rede, segurança e observabilidade no OpenShift Local.

## Início rápido

1. Ler [instalação](docs/INSTALACAO-CRC.md) e [requisitos](docs/REQUISITOS.md).
2. Conferir contexto e recursos com `bash scripts/preflight.sh` (somente leitura).
3. Validar fontes com `bash scripts/validate.sh` (kubectl, Python/PyYAML/jsonschema, Kubeconform 0.7.0 e ShellCheck).
4. Manter Operator, plano de controle e monitoramento na Application `service-mesh` do Argo CD; aplicar os cenários manualmente pelo projeto mesh-apps-lab.

## Entradas Kustomize

| Caminho | Uso |
|---|---|
| operator/ | Subscription 3.4.3, canal stable-3.4, aprovação automática |
| overlays/desenvolvimento/ | infraestrutura completa: Operator, namespaces, CNI, Istio v1.30.5, tag mesh-stable e monitores, com sync waves |
| monitoring/ | PodMonitor/ServiceMonitor RHOBS para Prometheus existente |
| optional/observability/ | infraestrutura, Kiali, tracing amostrado e alertas de segurança |
| optional/kiali/ | infraestrutura completa com Kiali, OAuth OpenShift e Prometheus existente |
| optional/tracing/ | alternativa ao overlay principal, com provider OTLP existente |
| assets/grafana/ | CRs de referência; integração no grafana-gitops |

Sincronizar a Application `service-mesh`; as waves ordenam as dependências. O tracing é **alternativa** à fonte completa da mesma Application, nunca um segundo proprietário do Istio. Os assets Grafana não são parte da base e não devem ter dois proprietários. Kiali é opcional; não instala Vault nem Prometheus/Grafana/Tempo adicionais. [Procedência dos schemas e versões](docs/PROCEDENCIA.md).

## Guias

- [Observabilidade, segurança e tracing](docs/OBSERVABILIDADE.md)

- [Kiali: instalação e grafo do mesh](docs/KIALI.md)

- [Arquitetura e Mermaid](docs/ARQUITETURA.md)
- [Primeiro teste manual](docs/01-primeiro-teste.md)
- [Exercícios e resultados esperados](docs/EXERCICIOS.md)
- [NetworkPolicy e Service Mesh](docs/NETWORKPOLICY-VS-SERVICE-MESH.md)
- [Métricas, PromQL e Grafana](docs/GRAFANA.md)
- [Diagnóstico](docs/TROUBLESHOOTING.md)
- [Rollback e limpeza](docs/ROLLBACK-E-CLEANUP.md)
- [Plano de testes](docs/PLANO-DE-TESTES.md)
- [Operação](docs/OPERACAO.md)
- [Aplicação manual dos cenários](docs/APLICACAO-MANUAL.md)
- [Evolução de PKI](docs/ROADMAP-VAULT.md)

Documentação operacional em Markdown/português. YAML, shell, JSON e testes mantêm extensões funcionais. Nenhuma credencial deve ser inserida nos exemplos, relatórios ou commits. Licença Apache 2.0, com avisos originais preservados.


## Aprender a configuração

Consulte o [guia comentado](docs/APRENDIZADO.md) para entender componentes, escolhas, testes positivos/negativos e reversão.
