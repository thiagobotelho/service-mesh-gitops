# NetworkPolicy e Service Mesh

| Controle | Unidade | Identidade usada | Negativo esperado |
|---|---|---|---|
| OVN NetworkPolicy | L3/L4, pods e portas TCP | labels de pod/namespace | timeout ou conexão recusada |
| PeerAuthentication STRICT | transporte proxy→proxy | certificado/identidade do Mesh | reset/erro TLS para plaintext |
| AuthorizationPolicy | método/caminho HTTP | principal SPIFFE do ServiceAccount | HTTP 403 |

O Service expõe 8000, mas o destino da NetworkPolicy é a porta 8080 do container. A origem permitida possui `app=sleep` no **mesmo namespace**. Regras de NetworkPolicy são aditivas: outra política que permita todos os ingressos pode invalidar o exercício. O script da fase 02 exige inventário exato de uma política, antes do teste.

Na defesa em profundidade, a política de scrape adiciona somente a porta 15090 para pods Prometheus em `observability-apps`. Ela não abre 8080 para sleep-denied. Não há default-deny de plataforma nem bloqueio de egress/DNS. Em 04/05 não há NetworkPolicy de laboratório para não mascarar mTLS ou L7.

O Service usa nome de porta `http`, permitindo classificação HTTP. AuthorizationPolicy permite exatamente `cluster.local/ns/mesh-lab/sa/sleep`, método GET e caminho /get. Alterar label do cliente não transfere sua identidade criptográfica. Permissões para alterar labels, ServiceAccounts ou workloads são administrativas e não são concedidas aos clientes.

Istio não observa um pacote eliminado antes de chegar ao proxy. Ausência de 403 no dashboard para bloqueio OVN é comportamento esperado. Para análise de rede, usar separadamente o Network Observability já existente e confirmar se a versão/configuração expõe eventos de drop; não inventar contagem de bloqueios a partir de métricas HTTP.
