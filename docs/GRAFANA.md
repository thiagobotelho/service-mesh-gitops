# Métricas e Grafana

O datasource existente é `prometheus-apps` (Prometheus-Apps), servido por `apps-monitoring-prometheus.observability-apps.svc:9090`. Não é necessário criar Prometheus, Grafana ou Tempo. A instância Grafana é selecionada por `dashboards=grafana`; pasta e dashboard usam CRDs `grafana.integreatly.org/v1beta1`, usados no provisionamento.

O MonitoringStack `apps-monitoring` e seu Prometheus usam os recursos **monitoring.rhobs/v1**, distintos dos recursos de mesmo nome do grupo monitoring.coreos.com. Os monitores deste laboratório usam o grupo RHOBS, `observability=platform`; seus namespaces recebem `observability=enabled`. Um monitor coreos.com poderia existir e ainda não ser coletado por este Prometheus. O PodMonitor coleta a porta nomeada `http-envoy-prom`, caminho `/stats/prometheus`, somente no container `istio-proxy`. Confirmar o nome na revisão instalada. Istiod usa `http-monitoring`, `/metrics`.

O JSON em `service-mesh-gitops/assets/dashboard-service-mesh.json` é a fonte revisável dos painéis. Os CRs de referência estão em `assets/grafana/`. A integração aprovada copia esses CRs para o overlay desenvolvimento de `grafana-gitops`. **Manter um único proprietário**: não aplicar assets/grafana separadamente. Eles não estão na base de infraestrutura.

## Consultas e unidade

```promql
sum by (destination_workload) (
  rate(istio_requests_total{destination_workload_namespace="mesh-lab",reporter="destination"}[2m])
)
histogram_quantile(0.95,
  sum by (le,destination_workload) (
    rate(istio_request_duration_milliseconds_bucket{destination_workload_namespace="mesh-lab",reporter="destination"}[2m])
  )
)
```

O histograma projetado usa milissegundos; não converter para segundos sem alterar o nome e a unidade do painel. A implantação precisa confirmar `_bucket`, `_sum`, `_count` e labels. As consultas HTTP selecionam `reporter="destination"`, evitando somar source e destination. `rate()` é calculada antes da agregação de contadores. Os quantis preservam `le`. `connection_security_policy="mutual_tls"` é consultada somente no reporter destination; confirme sua presença na versão instalada antes de interpretar o painel.

## Painéis entregues

RPS por destino; respostas HTTP; p50/p95/p99; tráfego por origem/destino/código; principais destinos; requisições com mTLS; scrape de proxies/Istiod; ausência de séries; proxies conectados e latência média. Filtros usam namespace, source_workload e destination_workload das séries de requisição. Os labels operacionais `job`, `pod` e `namespace` devem ser conferidos nos targets reais antes de considerar os painéis de saúde homologados.

## Verificar coleta e gráficos

```bash
# Dentro de mesh-apps-lab, depois da implantação autorizada:
bash scripts/generate-traffic.sh 60 2
bash scripts/verify-observability.sh
```

O verificador abre túnel somente em 127.0.0.1 e o encerra ao terminar. Exige séries reais e o CR do dashboard. Abra o Grafana e confira o estado do Operator, a janela temporal, as variáveis e os gráficos. O indicador `absent()` informa 1 quando faltam séries, e fica sem amostra quando elas existem.

O link relativo para Explore usa o datasource Tempo existente. Traces exigem ativar opcionalmente o módulo de tracing, confirmar serviço/porta do Collector, gerar requisições e consultar trace real no Tempo. HTTPbin/sleep não viram aplicações instrumentadas novas; a coleta é pelo proxy. Kiali pode ser avaliado depois; nenhum endereço Kiali é publicado sem instalação confirmada.

