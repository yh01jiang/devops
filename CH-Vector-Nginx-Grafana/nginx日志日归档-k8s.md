## 🚀 本脚本采用K8S部署为一个CronJob的方式：每日凌晨读取Nginx日志库中前一天的数据，聚合后写入日归档的数据表中，通过Grafana看板实现可视化。

### 1. 新增CronJob
wget https://StarsL.cn/kubedoor/nginx-daily2ch-cronjob.yaml
# 注意：数据库连接配置修改为你之前存储NGINX日志的ClickHouse（使用CH的TCP端口9000）, 可以不填表名。
kubectl apply -f nginx-daily2ch-cronjob.yaml

### 2. 部署完成后请手动执行一次JOB进行初始化历史数据
kubectl create job -n default --from=cronjob/nginx-daily2ch nginx-daily2ch-init1

## 3. 导入Grafana看板，注意数据源要选择之前NGINX请求日志分析看板的数据源。
https://StarsL.cn/kubedoor/nginx-daily2ch-grafana.json

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: nginx-daily2ch
  namespace: default
spec:
  # 每天凌晨12:30执行 (分 时 日 月 周)
  schedule: "30 0 * * *"
  timeZone: "Asia/Shanghai"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: nginx-daily2ch
            image: swr.cn-south-1.myhuaweicloud.com/starsl.cn/nginx-daily2ch:latest
            imagePullPolicy: Always
            command: ["python"]
            args: ["main.py"]
            env:
            # ClickHouse数据库连接配置（使用CH的TCP端口9000）
            - name: CLICKHOUSE_HOST
              value: "10.7.0.102"
            - name: CLICKHOUSE_PORT
              value: "9000"
            - name: CLICKHOUSE_DATABASE
              value: "nginxlogs"
            - name: CLICKHOUSE_USER
              value: "default"
            - name: CLICKHOUSE_PASSWORD
              value: "xxxxxxxx"
            resources:
              requests:
                memory: "50Mi"
                cpu: "200m"
              limits:
                memory: "1Gi"
                cpu: "1"
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 2
  failedJobsHistoryLimit: 1
  concurrencyPolicy: Forbid
```
3. 执行一次cronjob初始化
```bash
kubectl create job --from=cronjob/nginx-daily2ch nginx-daily2ch-init1
```

## 🔧  配置明细
🌈  正常情况只需要修改ClickHouse数据库的配置即可。
## 如果您有更多的自定义配置：.env文件预置了所有的配置，修改部署yaml文件的env来配置：
### 数据库连接配置：
* CLICKHOUSE_HOST: ClickHouse服务器地址
* CLICKHOUSE_PORT: ClickHouse服务器端口（默认9000）
* CLICKHOUSE_DATABASE: 数据库名称（填写实时入库的nginx日志所在的库）
* CLICKHOUSE_TABLE:指定要分析的表名（为空时处理所有_access结尾的表(即默认写入ClickHouse的原始nginx日志表)）
* CLICKHOUSE_USER: 数据库用户名
* CLICKHOUSE_PASSWORD: 数据库密码

### 表名配置：
* SOURCE_TABLE_SUFFIX: Nginx实时入库的源表后缀（默认：_access）
* ARCHIVE_TABLE_SUFFIX: 日归档表后缀（默认：_archive_daily）

### 时间周期配置：
* PEAK_PERIOD_MINUTES:高峰时段分析的时间窗口，单位分钟（默认：30）
* QPS_CALCULATION_SECONDS:QPS计算的时间间隔，单位秒（默认：10）
* TRAFFIC_CALCULATION_SECONDS:流量统计的时间间隔，单位秒（默认：10）

### 阈值配置：
* MIN_DOMAIN_REQUESTS: 域名分析的最小请求次数阈值（默认：20）
* SLOW_PATH_MIN_REQUESTS:慢路径TOP10分析的最小请求次数阈值（默认：1000）




## 基于NGINX请求日志的【日归档数据】分析看板json
```json
{
  "__inputs": [
    {
      "name": "DS_CK-10.7.0.102",
      "label": "CK-10.7.0.102",
      "description": "",
      "type": "datasource",
      "pluginId": "grafana-clickhouse-datasource",
      "pluginName": "ClickHouse"
    }
  ],
  "__elements": {},
  "__requires": [
    {
      "type": "grafana",
      "id": "grafana",
      "name": "Grafana",
      "version": "10.4.19"
    },
    {
      "type": "datasource",
      "id": "grafana-clickhouse-datasource",
      "name": "ClickHouse",
      "version": "4.3.2"
    },
    {
      "type": "panel",
      "id": "table",
      "name": "Table",
      "version": ""
    },
    {
      "type": "panel",
      "id": "timeseries",
      "name": "Time series",
      "version": ""
    }
  ],
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": {
          "type": "grafana",
          "uid": "-- Grafana --"
        },
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "description": "基于ClickHouse已入库的NGINX请求日志数据，按日维度进行聚合归档，生成每日请求数据的分析看板",
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": null,
  "links": [],
  "panels": [
    {
      "collapsed": false,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 7,
      "panels": [],
      "title": "每日高峰时段数据分析(每0.5小时为1个周期，取PV最大的周期的时段)",
      "type": "row"
    },
    {
      "datasource": {
        "type": "grafana-clickhouse-datasource",
        "uid": "${DS_CK-10.7.0.102}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "always",
            "spanNulls": false,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          }
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 1
      },
      "id": 1,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true
        },
        "tooltip": {
          "hideZeros": false,
          "mode": "multi",
          "sort": "desc"
        }
      },
      "pluginVersion": "12.0.1",
      "targets": [
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "editorType": "sql",
          "format": 0,
          "meta": {
            "builderOptions": {
              "columns": [],
              "database": "",
              "limit": 1000,
              "mode": "list",
              "queryType": "table",
              "table": ""
            }
          },
          "pluginVersion": "4.3.2",
          "queryType": "timeseries",
          "rawSql": "SELECT `日期` as time, `最大QPS`,`P99QPS` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time",
          "refId": "A"
        }
      ],
      "title": "高峰时段QPS曲线图",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "grafana-clickhouse-datasource",
        "uid": "${DS_CK-10.7.0.102}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "line",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "always",
            "spanNulls": false,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          },
          "unit": "ms"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 1
      },
      "id": 5,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true
        },
        "tooltip": {
          "hideZeros": false,
          "mode": "multi",
          "sort": "desc"
        }
      },
      "pluginVersion": "12.0.1",
      "targets": [
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "editorType": "sql",
          "format": 0,
          "meta": {
            "builderOptions": {
              "columns": [],
              "database": "",
              "limit": 1000,
              "mode": "list",
              "queryType": "table",
              "table": ""
            }
          },
          "pluginVersion": "4.3.2",
          "queryType": "timeseries",
          "rawSql": "SELECT `日期` as time, `平均RT`,`P99RT`,`P90RT` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time",
          "refId": "A"
        }
      ],
      "title": "高峰时段响应时间曲线图",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "grafana-clickhouse-datasource",
        "uid": "${DS_CK-10.7.0.102}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "bars",
            "fillOpacity": 60,
            "gradientMode": "opacity",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "never",
            "spanNulls": false,
            "stacking": {
              "group": "A",
              "mode": "percent"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          },
          "unit": "locale"
        },
        "overrides": []
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 0,
        "y": 9
      },
      "id": 3,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true
        },
        "tooltip": {
          "hideZeros": false,
          "mode": "multi",
          "sort": "desc"
        }
      },
      "pluginVersion": "12.0.1",
      "targets": [
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "editorType": "sql",
          "format": 0,
          "meta": {
            "builderOptions": {
              "columns": [],
              "database": "",
              "limit": 1000,
              "mode": "list",
              "queryType": "table",
              "table": ""
            }
          },
          "pluginVersion": "4.3.2",
          "queryType": "timeseries",
          "rawSql": "SELECT `日期` as time, `100ms以下`,`100-500ms`,`500-1kms`,`1k-2kms`,`2kms以上` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time",
          "refId": "A"
        }
      ],
      "title": "高峰时段各阶段响应时间分布占比",
      "type": "timeseries"
    },
    {
      "datasource": {
        "type": "grafana-clickhouse-datasource",
        "uid": "${DS_CK-10.7.0.102}"
      },
      "fieldConfig": {
        "defaults": {
          "color": {
            "mode": "palette-classic"
          },
          "custom": {
            "axisBorderShow": false,
            "axisCenteredZero": false,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "barAlignment": 0,
            "drawStyle": "bars",
            "fillOpacity": 0,
            "gradientMode": "none",
            "hideFrom": {
              "legend": false,
              "tooltip": false,
              "viz": false
            },
            "insertNulls": false,
            "lineInterpolation": "linear",
            "lineWidth": 1,
            "pointSize": 5,
            "scaleDistribution": {
              "type": "linear"
            },
            "showPoints": "auto",
            "spanNulls": false,
            "stacking": {
              "group": "A",
              "mode": "none"
            },
            "thresholdsStyle": {
              "mode": "off"
            }
          },
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": null
              },
              {
                "color": "red",
                "value": 80
              }
            ]
          },
          "unit": "binbps"
        },
        "overrides": [
          {
            "matcher": {
              "id": "byName",
              "options": "最大返回量"
            },
            "properties": [
              {
                "id": "custom.transform",
                "value": "negative-Y"
              }
            ]
          }
        ]
      },
      "gridPos": {
        "h": 8,
        "w": 12,
        "x": 12,
        "y": 9
      },
      "id": 4,
      "options": {
        "legend": {
          "calcs": [],
          "displayMode": "list",
          "placement": "bottom",
          "showLegend": true
        },
        "tooltip": {
          "hideZeros": false,
          "mode": "multi",
          "sort": "desc"
        }
      },
      "pluginVersion": "12.0.1",
      "targets": [
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "editorType": "sql",
          "format": 0,
          "meta": {
            "builderOptions": {
              "columns": [],
              "database": "",
              "limit": 1000,
              "mode": "list",
              "queryType": "table",
              "table": ""
            }
          },
          "pluginVersion": "4.3.2",
          "queryType": "timeseries",
          "rawSql": "SELECT `日期` as time, `最大请求量`,`最大返回量` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time",
          "refId": "A"
        }
      ],
      "title": "高峰时段每秒请求量与返回量",
      "type": "timeseries"
    },
    {
      "collapsed": true,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 17
      },
      "id": 9,
      "panels": [
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 0,
                "gradientMode": "none",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "auto",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "locale"
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "总UV"
                },
                "properties": [
                  {
                    "id": "custom.axisPlacement",
                    "value": "right"
                  },
                  {
                    "id": "custom.drawStyle",
                    "value": "bars"
                  },
                  {
                    "id": "custom.fillOpacity",
                    "value": 50
                  },
                  {
                    "id": "custom.gradientMode",
                    "value": "opacity"
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 2
          },
          "id": 2,
          "options": {
            "legend": {
              "calcs": [],
              "displayMode": "list",
              "placement": "bottom",
              "showLegend": true
            },
            "tooltip": {
              "hideZeros": false,
              "mode": "multi",
              "sort": "desc"
            }
          },
          "pluginVersion": "12.0.1",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 0,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "timeseries",
              "rawSql": "SELECT `日期` as time, `总UV`,`总PV` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time",
              "refId": "A"
            }
          ],
          "title": "每日总PV与总UV",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "bars",
                "fillOpacity": 60,
                "gradientMode": "opacity",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "never",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "none"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "locale"
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "5xx"
                },
                "properties": [
                  {
                    "id": "custom.axisPlacement",
                    "value": "right"
                  },
                  {
                    "id": "custom.drawStyle",
                    "value": "line"
                  },
                  {
                    "id": "custom.pointSize",
                    "value": 5
                  },
                  {
                    "id": "custom.showPoints",
                    "value": "always"
                  },
                  {
                    "id": "custom.fillOpacity",
                    "value": 80
                  },
                  {
                    "id": "custom.lineWidth",
                    "value": 2
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 12,
            "y": 2
          },
          "id": 6,
          "options": {
            "legend": {
              "calcs": [],
              "displayMode": "list",
              "placement": "bottom",
              "showLegend": true
            },
            "tooltip": {
              "hideZeros": false,
              "mode": "multi",
              "sort": "desc"
            }
          },
          "pluginVersion": "12.0.1",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 0,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "timeseries",
              "rawSql": "SELECT `日期` as time, `1xx`,`2xx`,`3xx`,`4xx`,`5xx` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time",
              "refId": "A"
            }
          ],
          "title": "每日各请求状态分布",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "continuous-GrYlRd"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "line",
                "fillOpacity": 60,
                "gradientMode": "opacity",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "always",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "normal"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  }
                ]
              },
              "unit": "percent"
            },
            "overrides": []
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 0,
            "y": 10
          },
          "id": 10,
          "options": {
            "legend": {
              "calcs": [],
              "displayMode": "list",
              "placement": "bottom",
              "showLegend": true
            },
            "tooltip": {
              "hideZeros": false,
              "mode": "multi",
              "sort": "desc"
            }
          },
          "pluginVersion": "12.0.1",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 0,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "timeseries",
              "rawSql": "SELECT `日期` as time, `请求成功率` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time",
              "refId": "A"
            }
          ],
          "title": "每日请求成功率(status<400)",
          "type": "timeseries"
        },
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "axisBorderShow": false,
                "axisCenteredZero": false,
                "axisColorMode": "text",
                "axisLabel": "",
                "axisPlacement": "auto",
                "barAlignment": 0,
                "drawStyle": "bars",
                "fillOpacity": 60,
                "gradientMode": "opacity",
                "hideFrom": {
                  "legend": false,
                  "tooltip": false,
                  "viz": false
                },
                "insertNulls": false,
                "lineInterpolation": "linear",
                "lineWidth": 1,
                "pointSize": 5,
                "scaleDistribution": {
                  "type": "linear"
                },
                "showPoints": "never",
                "spanNulls": false,
                "stacking": {
                  "group": "A",
                  "mode": "percent"
                },
                "thresholdsStyle": {
                  "mode": "off"
                }
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              },
              "unit": "locale"
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "5xx"
                },
                "properties": [
                  {
                    "id": "custom.axisPlacement",
                    "value": "right"
                  },
                  {
                    "id": "custom.drawStyle",
                    "value": "line"
                  },
                  {
                    "id": "custom.pointSize",
                    "value": 5
                  },
                  {
                    "id": "custom.showPoints",
                    "value": "always"
                  },
                  {
                    "id": "custom.fillOpacity",
                    "value": 80
                  },
                  {
                    "id": "custom.lineWidth",
                    "value": 2
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 8,
            "w": 12,
            "x": 12,
            "y": 10
          },
          "id": 11,
          "options": {
            "legend": {
              "calcs": [],
              "displayMode": "list",
              "placement": "bottom",
              "showLegend": true
            },
            "tooltip": {
              "hideZeros": false,
              "mode": "multi",
              "sort": "desc"
            }
          },
          "pluginVersion": "12.0.1",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 0,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "timeseries",
              "rawSql": "SELECT `日期` as time, `Windows`,`Android`,`iOS`,`MAC`,`其它` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time",
              "refId": "A"
            }
          ],
          "title": "每日访问设备操作系统分布",
          "type": "timeseries"
        }
      ],
      "title": "每日整体数据分析",
      "type": "row"
    },
    {
      "collapsed": true,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 18
      },
      "id": 19,
      "panels": [
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "align": "left",
                "cellOptions": {
                  "type": "color-background"
                },
                "inspect": false
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "time"
                },
                "properties": [
                  {
                    "id": "custom.width",
                    "value": 92
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 12,
            "w": 24,
            "x": 0,
            "y": 19
          },
          "id": 17,
          "options": {
            "cellHeight": "sm",
            "footer": {
              "countRows": false,
              "enablePagination": true,
              "fields": "",
              "reducer": [
                "sum"
              ],
              "show": false
            },
            "showHeader": true,
            "sortBy": []
          },
          "pluginVersion": "10.4.19",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 1,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "table",
              "rawSql": "SELECT `日期` as time, `慢path第一`,`慢path第二`,`慢path第三`,`慢path第四`,`慢path第五`,`慢path第六`,`慢path第七`,`慢path第八`,`慢path第九`,`慢path第十`  from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time desc",
              "refId": "A"
            }
          ],
          "title": "每日PV大于1000的URI请求,响应时间排行【格式: 响应时间:URI:请求次数】",
          "transformations": [
            {
              "id": "formatTime",
              "options": {
                "outputFormat": "yyyy-MM-DD",
                "timeField": "time",
                "useTimezone": true
              }
            }
          ],
          "type": "table"
        },
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "align": "left",
                "cellOptions": {
                  "type": "color-text"
                },
                "inspect": false
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "time"
                },
                "properties": [
                  {
                    "id": "custom.width",
                    "value": 92
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 12,
            "w": 24,
            "x": 0,
            "y": 31
          },
          "id": 16,
          "options": {
            "cellHeight": "sm",
            "footer": {
              "countRows": false,
              "enablePagination": true,
              "fields": "",
              "reducer": [
                "sum"
              ],
              "show": false
            },
            "showHeader": true,
            "sortBy": []
          },
          "pluginVersion": "10.4.19",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 1,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "table",
              "rawSql": "SELECT `日期` as time, `5xx第一`,`5xx第二`,`5xx第三`,`5xx第四`,`5xx第五`,`5xx第六`,`5xx第七`,`5xx第八`,`5xx第九`,`5xx第十` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time desc",
              "refId": "A"
            }
          ],
          "title": "每日各URI返回5XX次数排行【格式: 请求次数:URI】",
          "transformations": [
            {
              "id": "formatTime",
              "options": {
                "outputFormat": "yyyy-MM-DD",
                "timeField": "time",
                "useTimezone": true
              }
            }
          ],
          "type": "table"
        },
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "align": "left",
                "cellOptions": {
                  "type": "color-background"
                },
                "inspect": false
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "time"
                },
                "properties": [
                  {
                    "id": "custom.width",
                    "value": 92
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 12,
            "w": 24,
            "x": 0,
            "y": 43
          },
          "id": 18,
          "options": {
            "cellHeight": "sm",
            "footer": {
              "countRows": false,
              "enablePagination": true,
              "fields": "",
              "reducer": [
                "sum"
              ],
              "show": false
            },
            "showHeader": true,
            "sortBy": []
          },
          "pluginVersion": "10.4.19",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 1,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "table",
              "rawSql": "SELECT `日期` as time, `4xx第一`,`4xx第二`,`4xx第三`,`4xx第四`,`4xx第五`,`4xx第六`,`4xx第七`,`4xx第八`,`4xx第九`,`4xx第十` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time desc",
              "refId": "A"
            }
          ],
          "title": "每日各URI返回4XX次数排行【格式: 请求次数:URI】",
          "transformations": [
            {
              "id": "formatTime",
              "options": {
                "outputFormat": "yyyy-MM-DD",
                "timeField": "time",
                "useTimezone": true
              }
            }
          ],
          "type": "table"
        }
      ],
      "title": "每日整体异常请求数据排行榜",
      "type": "row"
    },
    {
      "collapsed": true,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 19
      },
      "id": 15,
      "panels": [
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "align": "left",
                "cellOptions": {
                  "type": "color-text"
                },
                "inspect": false
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "time"
                },
                "properties": [
                  {
                    "id": "custom.width",
                    "value": 94
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 12,
            "w": 24,
            "x": 0,
            "y": 20
          },
          "id": 12,
          "options": {
            "cellHeight": "sm",
            "footer": {
              "countRows": false,
              "enablePagination": true,
              "fields": "",
              "reducer": [
                "sum"
              ],
              "show": false
            },
            "showHeader": true,
            "sortBy": []
          },
          "pluginVersion": "10.4.19",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 1,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "table",
              "rawSql": "SELECT `日期` as time, `path第一`,`path第二`,`path第三`,`path第四`,`path第五`,`path第六`,`path第七`,`path第八`,`path第九`,`path第十` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time desc",
              "refId": "A"
            }
          ],
          "title": "每日各URI请求次数排行【格式: 请求次数:URI】",
          "transformations": [
            {
              "id": "formatTime",
              "options": {
                "outputFormat": "yyyy-MM-DD",
                "timeField": "time",
                "useTimezone": true
              }
            }
          ],
          "type": "table"
        },
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "align": "left",
                "cellOptions": {
                  "type": "color-background"
                },
                "inspect": false
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "time"
                },
                "properties": [
                  {
                    "id": "custom.width",
                    "value": 92
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 12,
            "w": 24,
            "x": 0,
            "y": 32
          },
          "id": 13,
          "options": {
            "cellHeight": "sm",
            "footer": {
              "countRows": false,
              "enablePagination": true,
              "fields": "",
              "reducer": [
                "sum"
              ],
              "show": false
            },
            "showHeader": true,
            "sortBy": []
          },
          "pluginVersion": "10.4.19",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 1,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "table",
              "rawSql": "SELECT `日期` as time, `IP-path第一`,`IP-path第二`,`IP-path第三`,`IP-path第四`,`IP-path第五`,`IP-path第六`,`IP-path第七`,`IP-path第八`,`IP-path第九`,`IP-path第十`  from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time desc",
              "refId": "A"
            }
          ],
          "title": "每日各用户IP请求URI次数排行【格式: 请求次数:URI:用户IP】",
          "transformations": [
            {
              "id": "formatTime",
              "options": {
                "outputFormat": "yyyy-MM-DD",
                "timeField": "time",
                "useTimezone": true
              }
            }
          ],
          "type": "table"
        },
        {
          "datasource": {
            "type": "grafana-clickhouse-datasource",
            "uid": "${DS_CK-10.7.0.102}"
          },
          "fieldConfig": {
            "defaults": {
              "color": {
                "mode": "palette-classic"
              },
              "custom": {
                "align": "left",
                "cellOptions": {
                  "type": "color-text"
                },
                "inspect": false
              },
              "mappings": [],
              "thresholds": {
                "mode": "absolute",
                "steps": [
                  {
                    "color": "green"
                  },
                  {
                    "color": "red",
                    "value": 80
                  }
                ]
              }
            },
            "overrides": [
              {
                "matcher": {
                  "id": "byName",
                  "options": "time"
                },
                "properties": [
                  {
                    "id": "custom.width",
                    "value": 94
                  }
                ]
              }
            ]
          },
          "gridPos": {
            "h": 12,
            "w": 24,
            "x": 0,
            "y": 44
          },
          "id": 14,
          "options": {
            "cellHeight": "sm",
            "footer": {
              "countRows": false,
              "enablePagination": true,
              "fields": "",
              "reducer": [
                "sum"
              ],
              "show": false
            },
            "showHeader": true,
            "sortBy": []
          },
          "pluginVersion": "10.4.19",
          "targets": [
            {
              "datasource": {
                "type": "grafana-clickhouse-datasource",
                "uid": "${DS_CK-10.7.0.102}"
              },
              "editorType": "sql",
              "format": 1,
              "meta": {
                "builderOptions": {
                  "columns": [],
                  "database": "",
                  "limit": 1000,
                  "mode": "list",
                  "queryType": "table",
                  "table": ""
                }
              },
              "pluginVersion": "4.3.2",
              "queryType": "table",
              "rawSql": "SELECT `日期` as time, `IP第一`,`IP第二`,`IP第三`,`IP第四`,`IP第五`,`IP第六`,`IP第七`,`IP第八`,`IP第九`,`IP第十` from ${db}.${project} prewhere $__timeFilter(`日期`) and `域名` = '${domain}'\r\norder by time desc",
              "refId": "A"
            }
          ],
          "title": "每日各用户IP请求次数排行【格式: 请求次数:用户IP】",
          "transformations": [
            {
              "id": "formatTime",
              "options": {
                "outputFormat": "yyyy-MM-DD",
                "timeField": "time",
                "useTimezone": true
              }
            }
          ],
          "type": "table"
        }
      ],
      "title": "每日整体用户请求数据排行榜",
      "type": "row"
    }
  ],
  "refresh": "",
  "schemaVersion": 39,
  "tags": [
    "nginx",
    "ClickHouse",
    "StarsL.cn"
  ],
  "templating": {
    "list": [
      {
        "current": {
          "selected": true,
          "text": "nginxlogs",
          "value": "nginxlogs"
        },
        "description": "",
        "hide": 2,
        "label": "db",
        "name": "db",
        "options": [
          {
            "selected": true,
            "text": "nginxlogs",
            "value": "nginxlogs"
          }
        ],
        "query": "nginxlogs",
        "skipUrlSync": false,
        "type": "textbox"
      },
      {
        "current": {},
        "datasource": {
          "type": "grafana-clickhouse-datasource",
          "uid": "${DS_CK-10.7.0.102}"
        },
        "definition": "show tables from $db",
        "hide": 0,
        "includeAll": false,
        "label": "项目",
        "multi": false,
        "name": "project",
        "options": [],
        "query": "show tables from $db",
        "refresh": 1,
        "regex": "/.*_archive_daily$/",
        "skipUrlSync": false,
        "sort": 0,
        "type": "query"
      },
      {
        "current": {},
        "datasource": {
          "type": "grafana-clickhouse-datasource",
          "uid": "${DS_CK-10.7.0.102}"
        },
        "definition": "select\n`域名`,sum(`总PV`) as pv\nFROM ${db}.${project}\n\tPREWHERE $__timeFilter(`日期`) \n\tgroup by `域名`\n        order by pv desc",
        "description": "仅展示日PV大于20的域名，ALL包含了所有域名的数据。",
        "hide": 0,
        "includeAll": false,
        "label": "域名",
        "multi": false,
        "name": "domain",
        "options": [],
        "query": "select\n`域名`,sum(`总PV`) as pv\nFROM ${db}.${project}\n\tPREWHERE $__timeFilter(`日期`) \n\tgroup by `域名`\n        order by pv desc",
        "refresh": 2,
        "regex": "/(?<value>.*)/",
        "skipUrlSync": false,
        "sort": 0,
        "type": "query"
      }
    ]
  },
  "time": {
    "from": "now-90d",
    "to": "now"
  },
  "timepicker": {
    "refresh_intervals": [
      "1m",
      "5m",
      "15m",
      "30m",
      "1h",
      "2h",
      "1d"
    ]
  },
  "timezone": "browser",
  "title": "NGINX请求日志分析看板【日归档数据】 20250616 StarsL.cn",
  "uid": "ceot3bcfrrfuob",
  "version": 23,
  "weekStart": ""
}

```


