#!/usr/bin/env bash
# Inventário somente em leitura, sem Secrets.
source "$(dirname "$0")/common.sh"
crc
"${OC[@]}" get clusterversion version -o jsonpath='{.status.desired.version}{"\n"}'
"${OC[@]}" get nodes
"${OC[@]}" adm top nodes
"${OC[@]}" get packagemanifest servicemeshoperator3 -n openshift-marketplace -o jsonpath='{range .status.channels[*]}{.name}{" "}{.currentCSV}{"\n"}{end}'
"${OC[@]}" get csv -n openshift-operators
"${OC[@]}" get crds -o name | grep -E 'istio|sail|monitoring' || true
"${OC[@]}" -n mesh-lab get deployments,services,networkpolicies --ignore-not-found
printf 'PASS: inventário concluído; não equivale à instalação ou homologação\n'
