# Arquitetura do laboratório

```mermaid
flowchart LR
  S["sleep / SA sleep"] --> N["OVN: NetworkPolicy L3/L4"]
  D["sleep-denied / SA própria"] --> N
  N --> E1["Envoy de origem"]
  E1 -->|"mTLS entre proxies"| E2["Envoy de destino: AuthorizationPolicy L7"]
  E2 --> H["httpbin:8080 / Service:8000"]
  E1 --> P["Prometheus Apps existente"]
  E2 --> P
  ID["Istiod + Istio CNI"] --> E1
  ID --> E2
  P --> G["Grafana existente: prometheus-apps"]
  E2 -. "OTLP opcional" .-> O["Collector existente → Tempo"]
```

O diagrama mostra camadas lógicas; NetworkPolicy opera sobre pacotes dos pods, sem identidade de ServiceAccount. O proxy aplica identidade SPIFFE e operações HTTP. O trecho app→proxy pode usar HTTP local enquanto proxy→proxy usa mTLS. `sleep-denied` tem seu próprio ServiceAccount, Deployment e seletores; não pode herdar a identidade de `sleep`.

O discovery selector limita o Mesh a namespaces `istio-discovery=mesh-crc`. A tag estável `mesh-crc` referencia o Istio de mesmo nome. O nome real de `IstioRevision` é consultado em `status.istioRevision` da tag, sem derivar o nome da versão. O destino usa `cluster.local`, valor configurado em `meshConfig.trustDomain`.

Plano de controle com uma réplica e três proxies modestos para estudo. Não há HA, garantia de capacidade nem SLA. A instalação do CNI é uma mudança de infraestrutura no nó e exige revisão separada, mesmo no laboratório.
