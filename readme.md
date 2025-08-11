## Tensuns(consul-manager)
参考文章： https://github.com/starsliao/TenSunS
🦄概述
后羿 - TenSunS(原ConsulManager)是一个使用Flask+Vue开发，基于Consul的WEB运维平台，弥补了Consul官方UI对Services管理的不足；并且基于Consul的服务发现与键值存储：实现了Prometheus自动发现多云厂商各资源信息；基于Blackbox对站点监控的可视化维护；以及对自建与云上资源的优雅管理与展示。

🌈功能描述
🎡1. Consul管理(比官方更优雅的Consul Web UI)
支持Consul Services的增删改查，可以批量删除Service。
直观的查看每个Services实例的信息，及整体Services的健康状态。
可以便捷的对Services实例的Tags、Meta、健康检查配置管理与查询。
💎2. 自建与云资源监控管理(ECS/RDS/Redis)
基于Consul实现Prometheus监控目标的自动发现。

✔当前已支持对接阿里云、腾讯云、华为云、AWS。

⭐支持多云ECS/RDS/Redis的资源、分组、标签自动同步到Consul并接入到Prometheus自动发现！(并提供云资源信息查询与自定义页面)
⭐支持多云ECS信息自动同步到JumpServer。
⭐支持多云账户余额与云资源到期日设置阈值告警通知。
⭐支持作为Exporter接入Prometheus：Prometheus增加TenSunS的JOB后可抓取云厂商的部分MySQL/Redis指标。(弥补原生Exporter无法获取部分云MySQL/Redis指标的问题)
✔支持自建主机/MySQL/Redis接入WEB管理，支持增删改查、批量导入导出，自动同步到Consul并接入到Prometheus监控！

✔提供了按需生成Prometheus配置与ECS/MySQL/Redis告警规则的功能。

✔设计了多个支持同步的各字段展示的Node_Exporter、Mysqld_Exporter、Redis_Exporter Grafana看板。

🚀3. 站点与接口监控管理
基于Consul + Prometheus + Blackbox_Exporter实现站点的自动发现与监控。

使用Web页面即可对监控目标增删改查，支持站点的分级分组查询管理。
支持对监控目标的批量删除与批量导入，数据实时同步到Consul。
提供了Blackbox的配置、Prometheus的配置以及Prometheus站点监控的告警规则。
设计了一个支持各分级分组字段展示的Blackbox_Exporter Grafana看板。
💫4. 高危漏洞采集与实时告警
增加了高危风险漏洞采集与实时告警通知功能。
功能开启即可采集最新30个漏洞列表。
每小时采集一次，发现新漏洞立即推送到群机器人。
支持企微、钉钉、飞书群机器人通知。
<img width="1244" height="502" alt="image" src="https://github.com/user-attachments/assets/792cfebc-549c-4015-8f2f-1616f28c1e42" />


#### 在tensuns自定义标签
<img width="751" height="749" alt="image" src="https://github.com/user-attachments/assets/2315f39b-3df4-4790-8f8e-f4cb9b23696b" />


<img width="778" height="771" alt="image" src="https://github.com/user-attachments/assets/a4013593-a368-4e16-aa0a-f955e1f02acc" />


<img width="1847" height="950" alt="image" src="https://github.com/user-attachments/assets/01297aae-250a-43b4-9f47-e1c200469acb" />

## 如何优雅的使用一个mysqld_exporter监控所有的MySQL实例.md
https://github.com/starsliao/TenSunS/blob/main/docs/%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E7%9A%84%E4%BD%BF%E7%94%A8%E4%B8%80%E4%B8%AAmysqld_exporter%E7%9B%91%E6%8E%A7%E6%89%80%E6%9C%89%E7%9A%84MySQL%E5%AE%9E%E4%BE%8B.md

## 使用一个redis_exporter监控所有的Redis实例.md
https://github.com/starsliao/TenSunS/blob/main/docs/%E4%BD%BF%E7%94%A8%E4%B8%80%E4%B8%AAredis_exporter%E7%9B%91%E6%8E%A7%E6%89%80%E6%9C%89%E7%9A%84Redis%E5%AE%9E%E4%BE%8B.md

## blackbox站点监控.md
https://github.com/starsliao/TenSunS/blob/main/docs/blackbox%E7%AB%99%E7%82%B9%E7%9B%91%E6%8E%A7.md

## ECS主机监控.md
https://github.com/starsliao/TenSunS/blob/main/docs/ECS%E4%B8%BB%E6%9C%BA%E7%9B%91%E6%8E%A7.md

## consul部署说明
https://github.com/starsliao/TenSunS/blob/main/docs/Consul%E9%83%A8%E7%BD%B2%E8%AF%B4%E6%98%8E.md


ECSdashboard：https://grafana.com/grafana/dashboards/8919                            Grafana 看板ID：8919
blackbox-export： Grafana 看板详情： https://grafana.com/grafana/dashboards/9965      Grafana 看板ID：9965
redis-export： Grafana 看板详情： https://grafana.com/grafana/dashboards/17507        Grafana 看板ID：17507
mysql-export： Grafana 看板详情： https://grafana.com/grafana/dashboards/17320        Grafana 看板ID：17320


## VM全家桶

参考文章： https://github.com/starsliao/VictoriaMetrics
参考文章： https://mp.weixin.qq.com/s/K20YBZ7pIIEPcpRJx4Kg8A

## 远程写入VM
收集多集群的信息，可以使用prometheus远程写入VM，或者prometheus的联邦集群，貌似目前主流的是远程写入VM，因为VM性能过大，资源消耗低。
https://prometheus.io/docs/prometheus/latest/configuration/configuration/

vmagent-vmalert-alertmanager代替 Prometheus-Grafana-Alertmanager，## 实现了vmagent-vmalert: 代替了prometheus的功能，

## argocd的应用学习
https://github.com/yh01jiang/devops/tree/main/devops-argocd-example

## flask的入门学习
https://github.com/yh01jiang/devops/tree/main/flask-demo


