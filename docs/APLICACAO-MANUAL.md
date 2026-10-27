# Aplicar cenários manualmente

As APIs de teste e suas políticas são operadas por este repositório, fora do Argo CD. A infraestrutura do Operator, Istio/CNI e monitoramento é mantida separadamente pelo projeto service-mesh-gitops.

## Primeiro cenário

Confirme contexto, namespace e os recursos preexistentes. Renderize antes de aplicar:

```bash
kubectl kustomize scenarios/01-baseline
oc apply -k scenarios/01-baseline
oc -n mesh-lab rollout status deployment/httpbin
oc -n mesh-lab rollout status deployment/sleep
oc -n mesh-lab rollout status deployment/sleep-denied
bash scripts/verify-samples.sh
```

Se já existirem objetos com esses nomes, compare seletores, portas e ServiceAccounts antes de assumir seu gerenciamento manual. Não exclua o namespace para resolver conflitos. Aplicar os exemplos é uma decisão do operador; a instalação da infraestrutura não os adota nem reinicia.

## Trocar de fase

oc apply não remove os recursos exclusivos da fase anterior. Antes da troca, remova apenas as políticas dos exercícios, identificadas pela marca laboratorio.sre.dev/proprietario=mesh-apps-lab. Não remova políticas de outros projetos.

```bash
oc -n mesh-lab delete networkpolicy \
  -l laboratorio.sre.dev/proprietario=mesh-apps-lab --ignore-not-found
# Execute as próximas exclusões somente se as CRDs de Istio existirem:
oc -n mesh-lab delete peerauthentications.security.istio.io,authorizationpolicies.security.istio.io \
  -l laboratorio.sre.dev/proprietario=mesh-apps-lab --ignore-not-found
# Fora da fase mTLS, retire sleep-plain somente se pertencer aos exercícios:
for tipo in deployment service serviceaccount; do
  dono="$(oc -n mesh-lab get "$tipo/sleep-plain" --ignore-not-found \
    -o jsonpath='{.metadata.labels.laboratorio\.sre\.dev/proprietario}')"
  if [ "$dono" = mesh-apps-lab ]; then
    oc -n mesh-lab delete "$tipo/sleep-plain" --ignore-not-found
  fi
done
# Selecione o cenário de destino e aguarde seus rollouts:
oc apply -k scenarios/05-authorization
```

Confira a propriedade de cada objeto antes de removê-lo. O cliente plaintext só é necessário na fase de mTLS.

Ao voltar ao baseline, remova também as políticas de Istio dos exercícios. Nas fases de mTLS e autorização isoladas, confirme que não restaram NetworkPolicies capazes de mascarar o resultado. As anotações dos templates controlam a injeção e disparam novos pods ao trocar de cenário.

Consulte [EXERCICIOS.md](EXERCICIOS.md), [PLANO-DE-TESTES.md](PLANO-DE-TESTES.md) e [ROLLBACK-E-CLEANUP.md](ROLLBACK-E-CLEANUP.md). Nenhum cenário é sincronizado automaticamente.
