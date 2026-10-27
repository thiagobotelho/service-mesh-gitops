#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
crc
for c in istios.sailoperator.io istiocnis.sailoperator.io istiorevisions.sailoperator.io istiorevisiontags.sailoperator.io; do
  "${OC[@]}" wait --for=condition=Established "crd/$c" --timeout=120s
done
"${OC[@]}" wait --for=condition=Ready istiocni/default --timeout=180s
"${OC[@]}" wait --for=condition=Ready istio/mesh-crc --timeout=180s
"${OC[@]}" get istio mesh-crc
"${OC[@]}" get istiorevisions,istiorevisiontags
"${OC[@]}" wait --for=jsonpath='{.status.state}'=Healthy istiorevisiontag/mesh-stable --timeout=120s
REVISAO=$("${OC[@]}" get istiorevisiontag mesh-stable -o jsonpath='{.status.istioRevision}')
[[ -n "$REVISAO" ]] || bloqueado 'tag mesh-stable ainda não tem revisão'
ATIVA=$("${OC[@]}" get istio mesh-crc -o jsonpath='{.status.activeRevisionName}')
[[ "$ATIVA" == "$REVISAO" ]] || bloqueado 'a tag não referencia a revisão ativa do Istio'
"${OC[@]}" get istiorevision "$REVISAO"
"${OC[@]}" -n istio-system get pods
"${OC[@]}" -n istio-cni get pods
printf 'PASS: plano de controle pronto; revisão real: %s\n' "$REVISAO"
