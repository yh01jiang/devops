docker exec -it grfana bash
grafana cli plugins install grafana-clickhouse-datasource
docker restart grafana
