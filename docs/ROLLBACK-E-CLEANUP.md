# Rollback e limpeza

1. Parar a geração de tráfego. Conferir os recursos manuais dos exercícios e o diff da infraestrutura no Argo CD.
2. Para rollback de segurança, remover as políticas exclusivas da fase corrente e aplicar manualmente o cenário anterior com oc apply -k. Voltar ao baseline remove os controles do laboratório; é uma decisão consciente de exercício, não remediação para produção.
3. Para sair do Mesh, aplicar manualmente 01-baseline, retirando as políticas anteriores, e aguardar os novos pods sem `istio-proxy`. Não remover CNI enquanto houver workloads dependentes em qualquer namespace.
4. Remover somente as Applications opcionais, sem cascata. Elas são entregues sem finalizer de exclusão de recursos. Verificar se uma mudança posterior adicionou finalizer antes de excluir.
5. Executar `mesh-apps-lab/scripts/cleanup.sh --confirmar-mesh-lab` para excluir apenas recursos marcados com `laboratorio.sre.dev/proprietario=mesh-apps-lab`. O script bloqueia enquanto existir Application reconciliando o repositório. Workloads sem a marca de propriedade e o namespace são preservados.
6. O cleanup de `service-mesh-gitops` remove somente seus monitores após conferência de propriedade. Não remove Operator, CRDs, CNI ou namespaces de forma automática. O CNI é potencialmente compartilhado e exige inventário global e aprovação própria.
7. Revisar manualmente remoção da tag `mesh-stable`, do Istio `mesh-crc` e depois IstioCNI `default`, somente se forem exclusivos do laboratório e não houver proxies dependentes. Aguardar a finalização de cada recurso antes do próximo. Não executar exclusão de CRDs para limpar o laboratório.
8. Se os CRs Grafana tiverem sido integrados, propor remoção da pasta/dashboard pelo repositório proprietário; preservar Grafana, Prometheus, Tempo, Keycloak e datasources.

Nenhuma rotina executa `oc delete project mesh-lab`, remove PVCs ou altera autenticação. Objetos manuais anteriores só entram no escopo se a adoção for explicitamente revisada. Um recurso sem label de propriedade não deve ser apagado pelo cleanup.

