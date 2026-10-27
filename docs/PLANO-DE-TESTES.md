# Plano de testes funcionais

Execute cada fase isoladamente e depois a composição. A tabela descreve critérios de aceite; não é um registro de execução.

| Fase | Procedimento | Resultado esperado |
|---|---|---|
| Baseline | sleep e sleep-denied fazem GET /get | ambos HTTP 200, sem proxy obrigatório |
| NetworkPolicy | sleep acessa httpbin:8000 | HTTP 200 |
| NetworkPolicy | sleep-denied acessa o mesmo destino | timeout/conexão recusada; resolução DNS funcional |
| Sidecar | aguardar rollouts e inspecionar containers | istio-proxy pronto nos três workloads |
| mTLS | dois clientes com proxy acessam destino STRICT | ambos HTTP 200 |
| mTLS negativo | sleep-plain sem proxy acessa destino STRICT | erro de transporte, reset ou erro TLS |
| Autorização | SA sleep faz GET /get | HTTP 200 |
| Autorização negativa | SA sleep-denied faz GET /get | HTTP 403 |
| Método/caminho | SA sleep faz POST /post ou GET /headers | HTTP 403 |
| Composição | sleep-denied com NetworkPolicy ativa | bloqueio de conectividade, sem exigir HTTP 403 |
| Composição | sleep faz POST /post | HTTP 403 por autorização L7 |
| Observabilidade | gerar tráfego, consultar Prometheus e abrir dashboard | séries com labels/unidades coerentes e gráficos preenchidos |

## Isolamento dos testes

- Não mantenha NetworkPolicy na fase de mTLS ou autorização isolada: ela pode mascarar o motivo de uma falha.
- Confira políticas aditivas e seletores antes de atribuir bloqueio ao OVN.
- Erro de DNS não comprova bloqueio de rede. O teste positivo do mesmo destino ajuda a identificar indisponibilidade da aplicação.
- Presença de sidecar não comprova criptografia: confirme STRICT, falha plaintext e telemetria mTLS quando disponível.
- Provisionar um dashboard não comprova coleta. Confira targets, séries, labels, unidade e janela temporal.

Os comandos e scripts de cada etapa estão em [EXERCICIOS.md](EXERCICIOS.md). Mantenha registros de execução fora do repositório de instalação, sem tokens, senhas, cookies ou kubeconfig.
