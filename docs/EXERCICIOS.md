# Exercícios por fase

Todos os resultados desta tabela são **esperados**, não resultados executados. Os testes dinâmicos aguardam implantação autorizada.

| Fase | Teste | Resultado esperado | Script no mesh-apps-lab |
|---|---|---|---|
| 01 | sleep e sleep-denied, GET /get | ambos HTTP 200, sem proxy | verify-samples.sh |
| 02 | sleep GET /get | HTTP 200 | test-networkpolicy.sh |
| 02 | sleep-denied GET /get | curl 7/28, HTTP 000; DNS continua funcional | test-networkpolicy.sh |
| 03 | proxies e comunicação | três pods com istio-proxy pronto; HTTP 200 | verify-samples.sh e inspeção abaixo |
| 04 | dois clientes com proxy | ambos HTTP 200 | test-mtls.sh |
| 04 | sleep-plain sem proxy | TLS/reset/empty reply, sem resposta HTTP | test-mtls.sh |
| 05 | SA sleep, GET /get | HTTP 200 | test-authorization.sh |
| 05 | SA sleep-denied, GET /get | HTTP 403 | test-authorization.sh |
| 05 | SA sleep, POST /post e GET /headers | HTTP 403 | test-authorization.sh |
| 06 | sleep-denied GET /get | falha L3/L4, sem 403 | test-defense-in-depth.sh |
| 06 | sleep POST /post | HTTP 403 L7 | test-defense-in-depth.sh |

```bash
oc --context=crc-admin --server=https://api.crc.testing:6443 -n mesh-lab get pods
# Esperado na fase 03+: httpbin/sleep/sleep-denied com 2/2 e container istio-proxy.
# Com istioctl da versão compatível disponível:
istioctl --context=crc-admin proxy-status
```

`test-mtls.sh` exige ausência de NetworkPolicy e AuthorizationPolicy. O `sleep-plain` reside no mesmo namespace, mas possui injeção explicitamente desabilitada e identidade própria: é um cliente fora do Mesh. O teste não usa NetworkPolicy para simular falha TLS. A política STRICT se limita ao seletor `app=httpbin`.

Cada teste rejeita divergências com código 1; pré-requisito ou acesso indisponível usa código 2 (`BLOCKED`). Erro de DNS (curl 6) nunca conta como bloqueio de NetworkPolicy. O teste positivo imediatamente anterior também detecta destino indisponível. Erros não reconhecidos exigem investigação; não ampliar arbitrariamente a lista para fazer o teste passar.

Para registrar execução real, criar arquivo Markdown `docs/reports/local-AAAA-MM-DD.md`, ignorado pelo Git. Anotar data, contexto, revisão de código e cenário, comandos e códigos de saída, evidências sanitizadas e resultado PASS/FAIL/BLOCKED/NOT_RUN. Não registrar cookies, tokens, kubeconfig ou dados de Secrets.
