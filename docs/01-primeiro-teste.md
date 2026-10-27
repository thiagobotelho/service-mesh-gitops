# Primeiro teste com os exemplos oficiais

Este é o fluxo **manual de estudo esperado**, antes da injeção e de políticas. Ele ainda não foi executado por esta implementação. No CRC auditado, mesh-lab já existe: não rodar estes comandos para sobrescrever os exercícios atuais. Revisar a migração/adoção primeiro. Para o fluxo GitOps, usar o cenário 01 e as cópias com SHA fixo.

```bash
# Após autorizar e resolver colisões; confirme antes crc-admin e api.crc.testing.
oc new-project mesh-lab
BASE=https://raw.githubusercontent.com/openshift-service-mesh/istio/release-1.24/samples
oc apply -n mesh-lab -f "$BASE/httpbin/httpbin.yaml"
oc apply -n mesh-lab -f "$BASE/sleep/sleep.yaml"
oc -n mesh-lab rollout status deployment/httpbin
oc -n mesh-lab rollout status deployment/sleep
oc -n mesh-lab exec deploy/sleep -c sleep -- curl -sS -o /dev/null -w '%{http_code}\n' http://httpbin:8000/get
```

Resultado **esperado**: HTTP 200, um container por pod e ausência de políticas de isolamento. A URL acima acompanha uma branch e serve para reproduzir o tutorial oficial; o GitOps usa os arquivos vendorizados no SHA indicado em PROCEDENCIA.md. O Service usa 8000, o container 8080. Não usar /dados: não é um endpoint oficial.

Ao migrar do tutorial manual ao GitOps, comparar o render, seletores imutáveis dos Deployments e identidade dos ServiceAccounts. Não excluir recursos automaticamente para contornar conflito de selector. Criar sleep-denied pela base versionada, jamais apenas trocar o nome do Deployment mantendo o selector de sleep.
