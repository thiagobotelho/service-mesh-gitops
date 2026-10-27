# Diagnóstico de falhas

| Sintoma | Conferência | Ação a revisar |
|---|---|---|
| BLOCKED por propriedade | check-ownership.sh; objetos com nomes conflitantes | revisar diff de adoção ou migrar exercícios; não apagar mesh-lab |
| Subscription pendente | Subscription/InstallPlan/CSV em openshift-operators | aprovar somente InstallPlan revisado; conferir acesso registry.redhat.io |
| CRD não encontrada | CSV e Established | aguardar Operator antes dos CRs; sem APIs do Service Mesh 2 |
| Pod permanece 1/1 | tag, revisão real, namespace discovery, anotação de injeção, webhook | conferir Istio/CNI; recriar pelo rollout após diff, sem SCC anyuid |
| Erro de init/proxy/SCC | eventos sanitizados; imagem; UID atribuído | manter restricted-v2 nos workloads; não conceder privilégios ao cliente |
| HTTP 403 para sleep | SA efetiva, trustDomain e caminho/método | corrigir principal específico; não liberar curinga |
| Timeout em fase 05 | NetworkPolicies remanescentes; prune da fase 02 | eliminar somente política do cenário anterior via Argo |
| Curl 6 | DNS | corrigir DNS; não classificar como sucesso de política |
| Prometheus sem série | grupo RHOBS, seletores e targets/ports | revisar PodMonitor e estado do scrape; aguardar tráfego e duas coletas |
| Dashboard vazio | datasource UID, reporter, labels, unidade e tempo | descobrir séries reais; não substituir ausência por números fictícios |
| Traces ausentes | provider no Istio, Telemetry e serviço OTLP existente | validar Collector e propagação de headers; não duplicar Tempo |

Comandos somente em leitura, no contexto local:

```bash
oc --context=crc-admin --server=https://api.crc.testing:6443 get istios,istiocnis,istiorevisions,istiorevisiontags
oc --context=crc-admin --server=https://api.crc.testing:6443 -n mesh-lab get pods,events,networkpolicies
oc --context=crc-admin --server=https://api.crc.testing:6443 -n mesh-lab get peerauthentications,authorizationpolicies
oc --context=crc-admin --server=https://api.crc.testing:6443 -n observability-apps get prometheus.monitoring.rhobs
```

Evitar publicar logs completos: podem conter headers de autenticação e metadados de usuários. Extrair apenas campos necessários para a falha. 

