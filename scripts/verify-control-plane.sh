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
REVISAO=$("${OC[@]}" get istiorevisiontag mesh-crc -o jsonpath='{.status.istioRevision}')
[[ -n "$REVISAO" ]] || bloqueado 'tag mesh-crc ainda não tem revisão'
"${OC[@]}" get istiorevision "$REVISAO"
"${OC[@]}" -n istio-system get pods
"${OC[@]}" -n istio-cni get pods
printf 'PASS: plano de controle pronto; revisão real: %s\n' "$REVISAO"
