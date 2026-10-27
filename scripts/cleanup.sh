#!/usr/bin/env bash
source "$(dirname "$0")/common.sh"
[[ ${1:-} == --confirmar-mesh-crc && $# == 1 ]] || bloqueado 'uso: cleanup.sh --confirmar-mesh-crc; retire primeiro Applications opcionais e todos os sidecars'
crc
apps=$("${OC[@]}" get applications.argoproj.io -A -o jsonpath='{.items[*].spec.source.repoURL}')
[[ "$apps" != *'/service-mesh-gitops'* ]] || bloqueado 'Application ainda reconcilia a infraestrutura'
# Não remover CNI compartilhado, Operator, CRDs ou namespaces automaticamente.
for item in 'istio-system podmonitors.monitoring.rhobs mesh-lab-envoy' 'istio-system servicemonitors.monitoring.rhobs mesh-crc-istiod'; do
  read -r ns tipo nome <<< "$item"
  dono=$("${OC[@]}" -n "$ns" get "$tipo/$nome" --ignore-not-found -o jsonpath='{.metadata.name}{" "}{.metadata.labels.laboratorio\.sre\.dev/proprietario}')
  [[ -z "$dono" || "$dono" == "$nome service-mesh-gitops" ]] || bloqueado "monitor preexistente sem propriedade: $tipo/$nome"
done
"${OC[@]}" delete podmonitors.monitoring.rhobs mesh-lab-envoy -n istio-system --ignore-not-found
"${OC[@]}" delete servicemonitors.monitoring.rhobs mesh-crc-istiod -n istio-system --ignore-not-found
printf 'PASS: monitores próprios removidos. Remoção de Istio/CNI exige revisão manual do inventário global; consulte docs/ROLLBACK-E-CLEANUP.md\n'
