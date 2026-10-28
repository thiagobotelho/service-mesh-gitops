# Infraestrutura por sync waves


Namespace precede Subscription; após Operator pronto e InstallPlan aprovado, vêm CNI, Istio, tag e monitores. Sync waves ordenam recursos dentro da Application; a aprovação automática do InstallPlan é responsabilidade do OLM, configurada na Subscription. Synced é convergência declarativa, Healthy depende das regras de saúde. A tag pode estar reconciliada e sem clientes.

## Procedimentos por responsabilidade

Use INSTALACAO-CRC.md para infraestrutura, OBSERVABILIDADE.md para logs/métricas/traces e mesh-apps-lab para exercícios. A label istio-discovery seleciona recursos observados; istio.io/rev seleciona a revisão de injeção. Antes de reiniciar um workload, confirme se a mudança depende da criação de novos pods ou pode ser distribuída pelo Istiod.
