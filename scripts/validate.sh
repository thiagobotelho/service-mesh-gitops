#!/usr/bin/env bash
set -euo pipefail
RAIZ=$(cd -- "$(dirname -- "$0")/.." && pwd)
for ferramenta in python3 kubectl shellcheck kubeconform; do command -v "$ferramenta" >/dev/null || { echo "BLOCKED: falta $ferramenta"; exit 2; }; done
while IFS= read -r -d '' script; do bash -n "$script"; shellcheck -S warning "$script"; done < <(find "$RAIZ/scripts" -name '*.sh' -print0)
while IFS= read -r -d '' entrada; do
  kubectl kustomize "$(dirname "$entrada")" | kubeconform -strict -summary -ignore-missing-schemas -kubernetes-version 1.35.0
done < <(find "$RAIZ" -name kustomization.yaml -print0)
python3 "$RAIZ/tests/validate.py"
python3 "$RAIZ/tests/test-scripts.py"
