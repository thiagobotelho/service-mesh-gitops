# Procedência, alterações e licenças

Samples oficiais: [openshift-service-mesh/istio](https://github.com/openshift-service-mesh/istio/tree/3d79ecd15be272817eed32a4a01c35ec923425df/samples), origem `release-1.24`, fixada no commit `3d79ecd15be272817eed32a4a01c35ec923425df`. O número da branch dos exemplos não define a versão do plano de controle: o catálogo local selecionado usa Istio v1.30.5.

`mesh-apps-lab/vendor/httpbin.yaml` e `vendor/sleep.yaml` são cópias byte a byte dos arquivos oficiais naquele commit. Os comentários e a licença Apache 2.0 foram preservados no idioma original por integridade legal. `LICENSE` preserva o texto legal; toda documentação operacional é Markdown em português.

As adaptações declaradas na base são: namespace mesh-lab; marca de propriedade sem alterar seletores; requests/limits; segurança compatível com restricted-v2; anotação de injeção e orçamento do proxy; imagens fixadas por digest observado nos pods locais dos mesmos samples em 26/10/2026. Isso **modifica o render**, sem alterar as cópias originais. A disponibilidade futura do registry e outras arquiteturas não foi testada.

`sleep-denied` deriva de sleep com Deployment, Service, labels, seletores e ServiceAccount independentes. O cliente de fase 04 `sleep-plain` também deriva do mesmo sample, sem sidecar. Não há API de aplicação desenvolvida para este laboratório.

Schemas Sail: extraídos de `chart/crds` de [sail-operator 3.4.3](https://github.com/openshift-service-mesh/sail-operator/tree/da74bf7e335a481561dbca5191febf8ca1f2a8cc/chart/crds), commit `da74bf7e335a481561dbca5191febf8ca1f2a8cc`, versão v1 de cada CRD. JSON Schema valida tipos e valores; não substitui validação de admissão, CEL, webhooks ou compatibilidade dos charts. As descrições textuais dos schemas foram removidas para reduzir tamanho, preservando restrições estruturais. Schemas de monitoramento/Grafana/OLM foram extraídos das CRDs públicas instaladas no CRC; somente schema, sem instâncias ou Secrets.

## Fontes consultadas

- [Instalação OSSM 3.4](https://docs.redhat.com/en/documentation/red_hat_openshift_service_mesh/3.4/html/installing/ossm-installing-service-mesh).
- [Injeção e revisão](https://docs.redhat.com/en/documentation/red_hat_openshift_service_mesh/3.4/html/installing/ossm-sidecar-injection).
- [Compatibilidade e ciclo de vida](https://access.redhat.com/support/policy/updates/openshift_operators).
- [Schemas Sail 3.4.3](https://github.com/openshift-service-mesh/sail-operator/tree/da74bf7e335a481561dbca5191febf8ca1f2a8cc).
- [Métricas Istio](https://istio.io/latest/docs/reference/config/metrics/). A página acompanha a versão corrente: confirme a unidade do histograma na instalação.
- [Implementação de métricas na linha 1.30](https://github.com/istio/proxy/blob/release-1.30/source/extensions/filters/http/istio_stats/istio_stats.cc): define histograma de duração em milissegundos; ainda requer confirmação no scrape real.
