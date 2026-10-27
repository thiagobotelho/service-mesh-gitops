#!/usr/bin/env bash
set -euo pipefail
OC=(oc --context=crc-admin --server=https://api.crc.testing:6443 --request-timeout=15s)
falhar() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
bloqueado() { printf 'BLOCKED: %s\n' "$*" >&2; exit 2; }
crc() {
  command -v oc >/dev/null || bloqueado 'oc não está disponível'
  local servidor
  servidor=$(oc --context=crc-admin config view --minify -o jsonpath='{.clusters[0].cluster.server}')
  [[ "$servidor" == https://api.crc.testing:6443 ]] || bloqueado 'contexto crc-admin não aponta ao CRC local'
  [[ $("${OC[@]}" get nodes -o jsonpath='{.items[*].metadata.name}') == crc ]] || bloqueado 'topologia diferente do CRC de nó único'
  "${OC[@]}" whoami >/dev/null
}
sem_politicas_rede() {
  [[ $("${OC[@]}" -n mesh-lab get networkpolicies -o name) == '' ]] || bloqueado 'há NetworkPolicy; isole primeiro o teste de mTLS/L7'
}
chamar() {
  local origem=$1 metodo=$2 caminho=$3
  set +e
  HTTP=$("${OC[@]}" -n mesh-lab exec "deployment/$origem" -c sleep -- curl --noproxy '*' --connect-timeout 3 --max-time 6 -sS -o /dev/null -w '%{http_code}' -X "$metodo" "http://httpbin.mesh-lab.svc.cluster.local:8000$caminho" 2>/dev/null)
  RC=$?
  set -e
  HTTP=${HTTP//$'\r'/}
}
http_esperado() {
  local esperado=$1; shift
  chamar "$@"
  [[ "$RC" == 0 && "$HTTP" == "$esperado" ]] || falhar "$*: esperado HTTP $esperado; obtido HTTP $HTTP, código $RC"
  printf 'PASS: %s → HTTP %s\n' "$*" "$HTTP"
}
sem_http() {
  local codigos=$1; shift
  chamar "$@"
  [[ "$HTTP" == 000 && " $codigos " == *" $RC "* ]] || falhar "$*: esperada falha de transporte; obtido HTTP $HTTP, código $RC"
  printf 'PASS: %s → falha de transporte (curl %s); não é HTTP 403\n' "$*" "$RC"
}
proxies() {
  local n nomes
  for n in httpbin sleep sleep-denied; do
    "${OC[@]}" -n mesh-lab rollout status "deployment/$n" --timeout=120s
    nomes=$("${OC[@]}" -n mesh-lab get pods -l "app=$n" -o jsonpath='{.items[*].spec.containers[*].name}')
    [[ " $nomes " == *' istio-proxy '* ]] || falhar "proxy ausente em $n"
  done
}
