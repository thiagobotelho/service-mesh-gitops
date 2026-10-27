#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
crc
command -v curl >/dev/null || bloqueado 'curl não está disponível'
command -v python3 >/dev/null || bloqueado 'python3 não está disponível'
PORTA=${1:-19090}
[[ "$PORTA" =~ ^[0-9]+$ ]] && (( PORTA >= 1024 && PORTA <= 65535 )) || falhar 'porta local inválida'
# Verifica CR provisionado. O preenchimento visual dos painéis ainda exige navegador.
"${OC[@]}" -n grafana get grafanadashboard service-mesh-crc -o jsonpath='{.status.conditions}{"\n"}'
"${OC[@]}" -n observability-apps port-forward --address=127.0.0.1 service/apps-monitoring-prometheus "$PORTA:9090" >/dev/null 2>&1 &
PF=$!
trap 'kill "$PF" 2>/dev/null || true; wait "$PF" 2>/dev/null || true' EXIT
PRONTO=0
for ((i=0; i<20; i++)); do
  kill -0 "$PF" 2>/dev/null || bloqueado 'túnel local não iniciou; porta ocupada ou acesso indisponível'
  if curl -fsS --max-time 2 "http://127.0.0.1:$PORTA/-/ready" >/dev/null; then PRONTO=1; break; fi
  sleep 1
done
[[ "$PRONTO" == 1 ]] || bloqueado 'Prometheus não ficou pronto'
for CONSULTA in  'istio_requests_total{destination_workload_namespace="mesh-lab",reporter="destination"}'  'istio_request_duration_milliseconds_bucket{destination_workload_namespace="mesh-lab",reporter="destination"}'  'istio_request_duration_milliseconds_sum{destination_workload_namespace="mesh-lab",reporter="destination"}'  'istio_request_duration_milliseconds_count{destination_workload_namespace="mesh-lab",reporter="destination"}'  'istio_requests_total{destination_workload_namespace="mesh-lab",reporter="destination",connection_security_policy="mutual_tls"}'  'up{namespace="mesh-lab"}'; do
  curl -fsS --max-time 5 --get --data-urlencode "query=$CONSULTA" "http://127.0.0.1:$PORTA/api/v1/query" | python3 -c '
import sys,json
r=json.load(sys.stdin)
if r.get("status")!="success" or not r.get("data",{}).get("result"):sys.exit(2)
for x in r["data"]["result"]:print(x.get("metric"),x.get("value"))
'
  printf 'PASS: série encontrada: %s\n' "$CONSULTA"
done
printf 'PENDENTE: conferir os gráficos no Grafana e revisar todos os labels; CR existente não prova dados visuais\n'
