# Operar e diagnosticar o mesh

## Componentes e fontes

| Informação | Fonte | Interface |
|---|---|---|
| Topologia HTTP, mTLS e configurações | Istiod e Prometheus de aplicações | Kiali |
| Métricas e alertas de workloads | MonitoringStack apps-monitoring | Grafana e Prometheus Apps |
| Logs JSON dos proxies | OpenShift Logging, tenant application | Kiali Logs, Observe Logs e Grafana |
| Decisões de NetworkPolicy | Auditoria OVN, tenant audit | Observe Logs e Grafana Loki-Audit |
| Fluxos e NetworkEvents | Network Observability e seu Loki dedicado | Network Traffic |
| Spans HTTP amostrados | Envoy → Collector OTLP → Tempo | Kiali e Grafana Tempo |

O Prometheus da plataforma não recebe automaticamente as métricas da MonitoringStack. O Loki de fluxos do Network Observability é separado do LokiStack do OpenShift Logging. Não trate essas fontes como intercambiáveis.

## Instalar o perfil completo

Pré-requisitos: mesh instalado, Collector de `opentelemetry-gitops`, Tempo de `tempo-gitops`, MonitoringStack de `prometheus-gitops`, Logging de `loki-gitops` e Grafana de `grafana-gitops`.

No checkout de `argocd-gitops`:

```bash
oc apply -k optional/service-mesh-observability
oc -n openshift-gitops get application service-mesh
oc -n istio-system get kiali,telemetry,prometheusrule
```

O perfil seleciona `service-mesh-gitops/optional/observability` na mesma Application, sem duplicar Istio/CNI/Kiali. Não reaplique o perfil sem observabilidade em seguida: ele troca a fonte da Application. O prune desativado exige remoção explícita dos recursos que deixarem o Git.

Os logs JSON são configuração do mesh na base. Alertas, tracing e permissões adicionais do Kiali são opcionais neste perfil. A Role de descoberta do Kiali permite apenas leitura de MutatingWebhookConfigurations para associar tags às revisões; não concede escrita nem leitura de Secrets. A consulta ao Tempo usa a ServiceAccount Kiali e o papel de leitura do tenant dev mantido por `tempo-gitops`.

## Investigar uma falha

1. Confirme hora, namespace, IP atual e identidade do cliente. Pods recriados podem mudar de IP.
2. Execute imediatamente antes uma chamada que deve funcionar.
3. Confira NetworkPolicy/OVN se a conexão não chega ao destino.
4. Confira o log do proxy do destino para rejeições de protocolo/mTLS ou autorização.
5. Correlacione request_id e trace_id quando disponíveis. Ausência de trace não comprova ausência de chamada: a coleta é amostrada e falhas pré-HTTP podem não gerar spans.

| Evidência | Interpretação |
|---|---|
| OVN verdict=drop com IP/porta correspondentes | Descarte de rede; isolamento de namespace não identifica uma policy DENY explícita |
| response_code_details=filter_chain_not_found | Nenhuma cadeia de filtros compatível; correlacione mTLS, protocolo e SNI |
| response_code_details com rbac_access_denied | Recusa de autorização do proxy |
| HTTP 403 sem esse detalhe | Pode ser resposta da aplicação; não atribua automaticamente ao mesh |
| HTTP 503 e flags de upstream | Investigue conexão, destino, endpoints e TLS |
| DNS falhou | Não conta como confirmação de bloqueio NetworkPolicy |

### Logs

```bash
oc -n mesh-lab logs deployment/httpbin -c istio-proxy --since=10m --tail=100
```

O formato JSON inclui endereços, código HTTP, flags, motivo, duração, identidade TLS, request_id e trace_id. Método/caminho podem estar ausentes em falhas anteriores ao HTTP. O caminho é registrado sem query string; headers de autorização, cookies e corpos não são coletados. Trate os demais identificadores conforme sua política de retenção.

No Kiali: Workloads → destino → Logs → sidecar-proxy. Um curl executado com oc exec escreve no terminal do operador, não automaticamente no log do container cliente. Na visão Envoy, Clusters/Listeners/Routes mostram configuração, não histórico de decisões.

As consultas LogQL de referência ficam em [loki-gitops/queries/mesh-network-security.json](https://github.com/thiagobotelho/loki-gitops/blob/main/queries/mesh-network-security.json). As mesmas consultas são persistidas nos painéis do dashboard Segurança do Mesh e NetworkPolicy, provisionado pelo Grafana no perfil desenvolvimento. O datasource Loki-Audit lê o tenant audit; ao ampliar a coleta de auditoria, revise quem pode usar esse datasource.

### Métricas e alertas

```promql
sum by (source_workload,connection_security_policy,response_code) (
  istio_requests_total{reporter="destination",destination_workload_namespace="mesh-lab"}
)
```

Consulte no Prometheus Apps ou Grafana. `connection_security_policy="mutual_tls"` é evidência para as requisições observadas, não uma garantia sobre todos os caminhos. Contadores de listener/TLS são habilitados seletivamente; ausência de séries deve ser apresentada como sem dados, não zero.

Os alertas 5xx usam janela de 10 minutos, volume mínimo de 100 chamadas, proporção acima de 5% e persistência de 10 minutos. Recusas 403 usam janela de 15 minutos, mínimo de 200 chamadas, proporção acima de 30% e persistência de 15 minutos. O namespace mesh-lab é excluído para não notificar recusas intencionais. Ajuste exclusão e limiares antes de usar em outras aplicações. A MonitoringStack avalia as regras; entrega de notificações depende de configurar um Alertmanager/receiver.

Valide regras sem gerar tráfego ou notificações:

```bash
python3 tests/test-alerts.py
```

Requer promtool no PATH. O teste usa séries sintéticas locais para cobrir disparo, tempo mínimo, baixo volume e exclusão do namespace dos exercícios.

### Tracing

O namespace do Collector deve corresponder aos discoverySelectors do Istiod. O overlay desenvolvimento de opentelemetry-gitops fornece `istio-discovery: mesh-crc`; essa label permite descoberta do Service, sem injetar proxy. Confira os logs do Istiod se o provider OTLP não aparecer na configuração Envoy.

O perfil usa Telemetry no namespace raiz do mesh, provider otel-existente e amostragem de 10%. Aplicações precisam propagar o contexto de tracing entre chamadas para preservar um trace distribuído. A injeção de proxy não instrumenta métodos internos nem consultas ao banco.

No Kiali, abra o workload e consulte Traces; no Grafana, use Tempo. Links externos usam a Route Grafana do perfil CRC: ajuste-a para seu domínio. TLS para Tempo permanece validado. Para validar um trace específico, envie uma chamada com contexto W3C conhecido e consulte o ID no backend, sem registrar credenciais.

## Transição entre testes

O Envoy pode reutilizar conexões estabelecidas antes de restringir uma NetworkPolicy. Um novo curl não garante uma nova conexão proxy→destino. No repositório `mesh-apps-lab`, consulte a transição de cenários e use o teste com `--recriar-cliente` quando precisar renovar somente o cliente negativo. Não limpe conntrack do nó nem reinicie workloads de outros projetos.

## Referências

- [Access logs Istio](https://istio.io/latest/docs/tasks/observability/logs/access-log/)
- [Kiali com Tempo](https://kiali.io/docs/configuration/external-services/tracing/tempo/)
- [NetworkPolicy e conexões existentes](https://kubernetes.io/docs/concepts/services-networking/network-policies/#networkpolicy-and-connections)
