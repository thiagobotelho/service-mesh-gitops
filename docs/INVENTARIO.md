# Inventário e decisões

Leitura em 26/10/2026, identidade pessoal autenticada thiagobotelho. Nenhum repositório de organização consultado. O repositório privado de estudos foi lido localmente; seu conteúdo não é republicado.

| Repositório público | HEAD padrão consultado | Decisão |
|---|---|---|
| [openshift-local-installer](https://github.com/thiagobotelho/openshift-local-installer) | `283de7624d1d246596e094cb77986faac42ad71b` | Documentar módulo opcional e capacidade |
| [argocd-gitops](https://github.com/thiagobotelho/argocd-gitops) | `6aef6988632f08da052d9bcec2e1bfff1b4a3cf4` | Proposta de Applications opcionais, fora da base |
| [prometheus-gitops](https://github.com/thiagobotelho/prometheus-gitops) | `4ebaef9a2da2683355c2e70bea5d3bd9ce55d63d` | Reutilizar MonitoringStack; esclarecer grupo RHOBS |
| [grafana-gitops](https://github.com/thiagobotelho/grafana-gitops) | `c20b799b4e8b11cbb281b81d0e9de54c04767e64` | Proposta de pasta/dashboard somente em desenvolvimento |
| [tempo-gitops](https://github.com/thiagobotelho/tempo-gitops) | `4a344b9e3f6e3b7398ad2292a8d1ee98e401984c` | Sem mudança técnica; documentar tracing opcional |
| [opentelemetry-gitops](https://github.com/thiagobotelho/opentelemetry-gitops) | `e7fc0ecbb8cf29b41979de1cfae8911ae40c09f4` | Reutilizar OTLP existente; sem mudança de TLS/SSO |
| [network-observability-gitops](https://github.com/thiagobotelho/network-observability-gitops) | `6184bbd5e6ea3553267ad418bdffd03018075535` | Documentar diferença de fluxos L3/L4 e métricas HTTP |
| [client-ip-api-openshift](https://github.com/thiagobotelho/client-ip-api-openshift) | `1853102951647f9155651fd387a21a3618d2b0ce` | Sem mudança: finalidade distinta, não usar como workload deste lab |

Foram inspecionados README, árvore de fontes, workflows e manifestos aplicáveis: App-of-Apps, MonitoringStack, NetworkPolicies, datasources, pastas/dashboards, Collector e TempoMonolithic. Não foi executada auditoria de segurança completa dos nove projetos. No CRC, 12 Applications estavam Synced/Healthy; isso descreve a stack anterior, sem comprovar o novo laboratório.

Correção descoberta durante preparação: usar `monitoring.rhobs/v1`, porque o Prometheus do COO não seleciona os monitores do grupo coreos.com. Recursos de ambos os grupos coexistem no cluster. Label de namespace `observability=enabled`; label de PodMonitor/ServiceMonitor `observability=platform`.

Os dois novos repositórios não existiam na consulta inicial e já foram publicados. Em 27/10/2026, as sete integrações nos projetos existentes foram mescladas após CI aprovado. As referências acima preservam o inventário inicial; os commits finais e PRs estão no [relatório atualizado](RELATORIO-FINAL.md).
