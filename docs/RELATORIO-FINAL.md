# Relatório da preparação e integração do laboratório

Atualização: 27/10/2026. O laboratório está versionado e integrado aos projetos pessoais existentes. A instalação do Mesh e sua homologação funcional permanecem pendentes.

## Repositórios e fontes

- [service-mesh-gitops](https://github.com/thiagobotelho/service-mesh-gitops): Operator OSSM 3, Istio/CNI v1.30.5, tag e descoberta, monitores RHOBS, tracing opcional, dashboard e guias.
- [mesh-apps-lab](https://github.com/thiagobotelho/mesh-apps-lab): samples oficiais fixados por SHA, clientes distintos e seis cenários de NetworkPolicy, Mesh, mTLS e autorização.

O conteúdo foi revisado para credenciais. Nenhuma senha, token, chave privada ou client secret foi publicado. Documentação e commits em português. Não foram criadas aplicações novas para substituir httpbin/sleep nem instâncias adicionais de Prometheus/Grafana/Tempo.

## Integrações concluídas

| Projeto | PR integrado | Conteúdo |
|---|---|---|
| openshift-local-installer | [#2](https://github.com/thiagobotelho/openshift-local-installer/pull/2) | Referência e pré-requisitos do laboratório opcional |
| argocd-gitops | [#3](https://github.com/thiagobotelho/argocd-gitops/pull/3) | Quatro Applications opcionais e guia OpenShift–Keycloak |
| prometheus-gitops | [#2](https://github.com/thiagobotelho/prometheus-gitops/pull/2) | Seletores e grupo RHOBS para métricas Istio/Envoy |
| grafana-gitops | [#2](https://github.com/thiagobotelho/grafana-gitops/pull/2) | Pasta e dashboard no overlay desenvolvimento |
| tempo-gitops | [#1](https://github.com/thiagobotelho/tempo-gitops/pull/1) | Reutilização do Tempo e validação de tracing |
| opentelemetry-gitops | [#2](https://github.com/thiagobotelho/opentelemetry-gitops/pull/2) | Recepção opcional de spans no Collector existente |
| network-observability-gitops | [#2](https://github.com/thiagobotelho/network-observability-gitops/pull/2) | Distinção entre bloqueios L3/L4 e autorização L7 |

Os sete PRs foram mesclados após CI aprovado no respectivo HEAD. O CI dos sete commits de merge também concluiu com sucesso. As bases e commits efetivos estão no histórico dos PRs; os HEADs do inventário representam a leitura inicial, não o estado após integração. A branch utilizada é laboratorio/service-mesh-crc.

## Mesh e Argo CD

As quatro Applications estão versionadas em [argocd-gitops/optional/service-mesh](https://github.com/thiagobotelho/argocd-gitops/tree/main/optional/service-mesh), fora do App-of-Apps e sem sincronização automática. Na consulta de 27/10 não havia Application do Mesh criada no Argo CD do CRC. Integrar os YAMLs não instala o Operator nem adota os workloads preexistentes.

O dashboard é gerenciado pelo overlay desenvolvimento de grafana-gitops. Não aplicar os assets de referência em paralelo para evitar dois proprietários dos mesmos CRs. O preenchimento real dos painéis depende da instalação e da coleta de métricas do Mesh.

## Autenticação OpenShift–Keycloak

O client confidencial openshift é versionado em keycloak-gitops/base/keycloak-config-realm.yaml. O provedor OAuth e a CA estão em argocd-gitops/bootstrap/crc-keycloak-provider.yaml, fora do overlay normal. A credencial permanece no Secret openshift-config/keycloak-openshift-client-secret, chave clientSecret, fora do Git.

A consulta de 27/10 confirmou o provedor no OAuth cluster e o Secret somente por metadados. Não repetiu login nem comparou valores de credenciais. O [guia de autenticação](https://github.com/thiagobotelho/argocd-gitops/blob/main/docs/AUTENTICACAO-KEYCLOAK-CRC.md) explica client, callback, claims, grupos e cuidados de reaplicação.

## Validações e evidências

- 18 pontos Kustomize novos e os renders dos projetos existentes passaram na preparação local.
- Schemas Kubernetes 1.35, Sail, políticas Istio, Grafana, RHOBS e OLM verificados; admissão/CEL/webhooks reais continuam pendentes.
- Contratos de erros rejeitam DNS/403 como prova de bloqueio OVN, limitam carga e bloqueiam contexto divergente.
- A API Prometheus aceitou as 12 consultas, mas não havia séries Istio. absent() produziu apenas sentinela de ausência.
- Hashes dos 111 arquivos inicialmente publicados foram comparados com fontes locais. CI real registrado em Actions e nos PRs.

## Estado do cluster e bloqueios

Em 26/10, a conferência final identificou cinco Applications Degraded por ResolutionFailed/ConstraintsNotSatisfiable nas Subscriptions. Em 27/10, as 12 Applications existentes estavam Healthy; não houve remediação OLM nesta integração. O incidente permanece histórico, sem atribuir causa não comprovada.

A adoção dos exercícios existentes httpbin/sleep em mesh-lab segue BLOCKED: não possuem a marca de propriedade do novo laboratório. intruso permanece fora da gestão. Nenhum Operator, CNI ou política do Mesh foi aplicado nesta etapa.

A matriz atual contém 14 PASS, 0 FAIL, 1 BLOCKED e 9 NOT_RUN. Ela não representa homologação funcional completa. Consultar [MATRIZ-VALIDACAO.md](MATRIZ-VALIDACAO.md).

## Próxima etapa

```bash
# Em mesh-apps-lab, somente leitura:
bash scripts/preflight.sh
bash scripts/check-ownership.sh
```

Após revisar/autorizar a adoção e a instalação no contexto crc-admin, seguir [INSTALACAO-CRC.md](INSTALACAO-CRC.md), sincronizar um cenário por vez com prune revisado e executar A–G com evidências reais. Tracing, Kiali, PKI externa, HA/DR e carga continuam pendentes ou fora desta fase.
