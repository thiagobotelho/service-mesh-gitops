# Kiali opcional

Kiali apresenta o grafo de serviços, métricas HTTP, uso de mTLS, logs dos proxies e validações das configurações Istio. O perfil reutiliza o Prometheus da MonitoringStack `apps-monitoring`; não instala outro Prometheus.

## Instalar com a mesma Application

Pré-requisitos: infraestrutura do mesh, MonitoringStack em `observability-apps`, monitores do mesh e acesso ao catálogo `redhat-operators`.

No checkout de `argocd-gitops`:

```bash
oc apply -k optional/service-mesh-kiali
oc -n openshift-gitops get application service-mesh
oc -n openshift-operators get subscription kiali-ossm
oc -n istio-system get kiali,pods,route
```

O perfil altera a fonte da Application `service-mesh` para `service-mesh-gitops/optional/kiali`. Operator, CNI, Istio, monitores e Kiali permanecem na mesma Application. A Subscription do Kiali utiliza o canal `stable` e aprovação automática, inclusive para atualizações futuras; `startingCSV` define apenas a versão inicial. As APIs dos exercícios continuam manuais.

## Acessar e visualizar

```bash
oc -n istio-system get route kiali -o jsonpath='https://{.spec.host}{"\n"}'
```

Abra a URL e entre pelo OpenShift. Se Keycloak estiver cadastrado como IdP do OpenShift, escolha esse provedor e use sua conta existente. Nenhuma conta ou senha adicional do Kiali é criada.

1. Abra **Traffic Graph** e selecione o namespace `mesh-lab`.
2. Selecione uma janela que contenha as chamadas dos exercícios, por exemplo os últimos 10 minutos.
3. Gere algumas requisições entre os clientes e o `httpbin`.
4. Habilite os indicadores de segurança/mTLS e examine códigos HTTP, taxa e latência.
5. Abra os detalhes do workload para consultar métricas, configurações e logs do proxy.

O grafo depende de tráfego no período consultado. Uma falha de handshake antes do HTTP pode não aparecer como requisição HTTP. O ícone de mTLS representa tráfego observado; confira também as políticas configuradas.

## Escopo e acesso

- OAuth do OpenShift e permissões Kubernetes do usuário controlam o acesso.
- A interface é somente de leitura; alterações devem ser feitas no Git.
- O escopo de descoberta usa namespaces com `istio-discovery: mesh-crc`, incluindo o namespace do control plane.
- A NetworkPolicy `allow-kiali-to-prometheus-apps` permite somente Pods com `app.kubernetes.io/name: kiali`, no namespace `istio-system`, consultar o Prometheus selecionado na porta 9090. Não altera as permissões existentes do Grafana ou Zabbix.
- A consulta ao Prometheus usa HTTP interno protegido pela política de rede. Não publique esse endpoint sem autenticação.
- Grafana e tracing não são integrados automaticamente neste perfil. Os serviços existentes permanecem disponíveis em suas interfaces.

## Diagnóstico

```bash
oc -n openshift-operators get subscription,installplan,csv
oc -n istio-system get kiali kiali -o yaml
oc -n istio-system logs deployment/kiali --tail=100
oc -n observability-apps get networkpolicy allow-kiali-to-prometheus-apps
```

Se não houver grafo, confira saúde dos alvos de scrape, URL do Prometheus no recurso Kiali, seletores da política e janela de consulta. O Prometheus da plataforma não contém automaticamente as séries desta MonitoringStack.

## Retirar o perfil

Antes de voltar para `optional/service-mesh` no repositório `argocd-gitops`, inventarie Kiali, Route, OAuthClient e recursos criados pelo operador. O prune está desativado: trocar a fonte não desinstala o Kiali. Remova explicitamente a instância após revisar seus recursos dependentes. Só remova o operador se não houver outras instâncias que dependam dele; preserve a infraestrutura do mesh e do Prometheus.

## Referências

- [Kiali no OpenShift Service Mesh 3.4](https://docs.redhat.com/en/documentation/red_hat_openshift_service_mesh/3.4/html/observability/kiali-operator-provided-by-red-hat)
- [Referência do recurso Kiali](https://kiali.io/docs/configuration/kialis.kiali.io/)
- [Indicadores de segurança](https://kiali.io/docs/features/security/)
