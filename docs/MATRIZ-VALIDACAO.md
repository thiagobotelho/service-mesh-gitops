# Matriz de validação

Data: 26/10/2026. PASS exige execução. Saídas esperadas dos tutoriais não contam como evidência.

| ID | Verificação | Estado | Evidência / pendência |
|---|---|---|---|
| INV-01 | Identidade e escopo pessoal de nove repositórios | PASS | conta thiagobotelho; HEADs registrados em inventário; privado não republicado |
| INV-02 | CRC e catálogo reais em leitura | PASS | crc-admin, api.crc.testing, OCP 4.22.1, OVN, stable-3.4/3.4.3 |
| COMP-01 | Compatibilidade documental | PASS | política oficial: linha 3.4 com OCP 4.22; catálogo fornece v1.30.5 |
| STAT-01 | Render de todos os pontos Kustomize | PASS | scripts/validate.sh; validação local |
| STAT-02 | Identidades, seletores, políticas e escopo por fase | PASS | tests/validate.py; sem controle L3 mascarando fase 04/05 |
| STAT-03 | Contratos de erros e carga limitada | PASS | tests/test-scripts.py; DNS/403 não contam como bloqueio OVN |
| STAT-04 | Sintaxe shell e ShellCheck | PASS | execução local com ShellCheck 0.11.0 |
| STAT-05 | YAML e JSON | PASS | parses locais; lint antes da publicação |
| STAT-06 | Schemas Sail/Grafana/RHOBS | PASS | extração oficial/CRDs; não substitui admissão no servidor |
| STAT-07 | Schemas Kubernetes 1.35 | PASS | Kubeconform 0.7.0 strict; CRDs validadas separadamente |
| OBS-00 | Sintaxe das 12 consultas PromQL | PASS | API real Prometheus aceitou; sem séries Istio; absent() retornou sentinela |
| CRC-OLM | Saúde final das Subscriptions existentes | FAIL | cinco Applications Synced/Degraded por ResolutionFailed/ConstraintsNotSatisfiable; catálogo não resolveu pacotes/canal das Subscriptions |
| OWN-01 | Adoção dos exercícios preexistentes | BLOCKED | httpbin/sleep sem marca de propriedade; revisar colisão antes de sincronizar |
| INT-01 | Publicação dos diffs nos sete existentes | NOT_RUN | propostas locais; nenhum commit ou PR realizado |
| CI-01 | GitHub Actions dos novos repositórios | PASS | pipelines de implementação concluídos; commits e runs no relatório final |
| A | Baseline sleep e sleep-denied HTTP 200 | NOT_RUN | implantação ainda não autorizada; recursos não aplicados |
| B | NetworkPolicy: 200 e timeout, DNS preservado | NOT_RUN | executar cenário 02 |
| C | Sidecar e plano de controle prontos | NOT_RUN | Operator/Istio/CNI ainda não instalados |
| D | STRICT, mTLS positivo e plaintext negativo | NOT_RUN | executar 04 sem NetworkPolicy/L7 |
| E | Identidade/método/caminho: 200/403 | NOT_RUN | executar 05 |
| F | Combinação L3/L4 e L7 | NOT_RUN | executar 06 |
| G | Séries Prometheus e gráficos reais no Grafana | NOT_RUN | gerar tráfego, consultar API e conferir visualmente |
| OPT-01 | Tracing via Collector/Tempo existente | NOT_RUN | módulo opcional; sem trace desta implantação |
| OPT-02 | Kiali, Vault/PKI externa, HA/DR/carga | NOT_RUN | fora desta fase; backlog explícito |

Há FAIL no inventário final da infraestrutura OLM existente. Nenhum teste dinâmico dos novos cenários foi executado. Isso não equivale a aprovação funcional. BLOCKED registra a colisão encontrada; NOT_RUN registra trabalho ainda não executado. Publicação de YAML e CI verde não homologam o laboratório no cluster.
