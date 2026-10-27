# Evolução: Vault, cert-manager e istio-csr

Este laboratório usa a emissão de certificados do próprio Mesh. Vault não é instalado nesta fase.

Antes de adotar PKI externa, estudar trust domain, raiz/intermediária, rotação, expiração, indisponibilidade da CA, armazenamento seguro, políticas mínimas do Vault e identidade do agente. Confirmar o estado de suporte/Technology Preview na versão efetiva da integração cert-manager/istio-csr; não tratar o exemplo como homologação.

Executar em fase separada: provar cadeia de confiança e SAN SPIFFE; testar rotação sem perda de tráfego; negar emissão a SA não autorizado; remover disponibilidade da CA temporariamente em teste controlado; validar rollback para a CA anterior sem misturar trust bundles. Registrar os resultados reais em Markdown. Não inserir root tokens, chaves privadas, unseal keys ou certificados privados nos repositórios.

Kiali, ingress externo, múltiplas revisões canário, políticas de egress, HA/DR e teste de carga são evoluções independentes, devem ser planejados em fases próprias.

