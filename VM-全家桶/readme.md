# VictoriaMetrics全家桶入门与K8S部署
<img width="1080" height="582" alt="image" src="https://github.com/user-attachments/assets/b702243e-4853-48cd-abb5-1d86c3960c6a" />


## 部署文件
本次将会部署以下组件:

 master
 ├── 0.vm-single.yaml
 ├── 1.kube-state-metrics.yaml
 ├── 1.node-exporter.yaml
 ├── 1.vmagent.yaml
 ├── 2.vmalert.yaml
 ├── 3.alertmanager.yaml
 ├── 4.alert-webhook.yaml
 └── 5.grafana.yaml

* vmagent是采集组件，负责采集指标；采集后远程写入VictoriaMetrics时序数据库。

* vmalert读取告警规则后，从VM查询数据进行评估，后发送给alertmanager进行告警；记录规则也会远程写入VM。

* vmagent + vmalert + VictoriaMetrics 组成了完整的Prometheus功能 + 远程存储。

* kube-state-metrics和node-exporter分别是采集K8S和主机指标的导出器。

* alert-webhook是Flask写的一个推送消息的组件，可以把alertmanager的告警根据路由规则推送给企微、钉钉、飞书。


## 快速安装
git clone https://github.com/starsliao/VictoriaMetrics.git
cd VictoriaMetrics
kubectl apply -f .


* 部署yaml文件后，以上所有组件将安装到K8S的monit命名空间，并接入各个组件、K8S和节点的监控。

* 你只需要登录grafana配置数据源并导入看板接口实现K8S与节点的监控。

* 装后以上所有组件默认接入到监控与自动发现，并且根据告警规则进行告警推送。

* 以下是各yaml文件的详细介绍描述，让您不仅仅是安装好VictoriaMetrics全家桶，还能明明白白的了解每个组件的关联、配置与作用。


### VictoriaMetrics：
* 时序数据库，存储所有的指标信息；可水平扩容的本地全量持久化存储方案。

* 对于低于每秒一百万个数据点的摄取率，官方建议使用单节点版本而不是集群版本。单节点版本可根据 CPU、内存和可用存储空间的数量进行扩展。单节点版本比集群版本更容易配置和操作，所以在使用集群版本之前要三思而后行。

kubectl apply -f 0.vm-single.yaml

* YAML文件注意事项：

-retentionPeriod=30d： 数据存储时长

resources： K8S资源限制

storageClassName: local-path  PV，PVC配置（当前使用本地主机存储，使用其它类型外部存储的请根据实际情况调整）,根据实际情况修改使用的storageClassName名称  

path: /k3s/data/vm-single 本地主机存储的本地路径,需提前创建目录  

nodeSelectorTerms ：根据实际情况修改本地主机存储的节点名 

storage： 存储大小

### node-exporter： 

* 采集Linux组件的指标.

* vmagent已经配置JOB自动发现资源。

kubectl apply -f 1.node-exporter.yaml

### kube-state-metrics

* 采集K8S的指标。
* vmagent已经配置JOB自动发现资源。

kubectl apply -f 1.kube-state-metrics_v2.12.0.yaml

### vmagent

* 负责对配置或者自动发现的JOB进行pull方式采集，也支持接收push进来的指标。

kubectl apply -f 1.vmagent.yaml

* YAML文件注意事项：

1. ConfigMap

* 兼容Prometheus的配置：采集间隔，JOB的配置（已经配置好了监控K8S和Node的支持自动发现的JOB）

* external_labels是Prometheus的外部系统标签，用于多个Prometheus接入同一个VictoriaMetrics时，区分不同的Prometheus。每个vmagent都必须配置，key是origin_prometheus，value是该vmagent的名称。

2. remoteWrite.url

* 远程写url,注意修改了vm存储的账号密码这里要同步修改。

* 如果服务端的vmagent和VM部署在同一个K8S下，url使用service地址，无需修改。

3. resources：K8S资源限制

### vmalert
* 读取告警规则，并查询VM时序数据库，触发告警则推送到alertmanager。

* 查询记录规则，并写入VM时序数据库。

kubectl apply -f 2.vmalert.yaml

* YAML文件注意事项：

* ConfigMap

* 兼容Prometheus的rule配置：各类告警规则,记录规则（已经配置好了监控K8S和Node的告警规则）

* rule规则中：`alert`是告警的名称，`annotations.at`是告警时@的人，`annotations.description`是告警的内容.

* -datasource.url： 查询的VM时序数据库地址

* -notifier.url： 通知的alertmanager地址

* -remoteWrite.url： 写入的VM时序数据库地址

* resources： K8S资源限制

### alertmanager

* alertmanager：接收触发的告警，并根据条件路由到不同的通知服务。

kubectl apply -f 3.alertmanager.yaml

* YAML文件注意事项：

1. ConfigMap

标准的alertmanager配置，注意webhook地址要配置alert-webhook的url。

alert-webhook的url的格式：

http://alert-webhook.monit/node/ddkey=钉钉群机器人ID

http://alert-webhook.monit/node/wckey=企微群机器人ID

2. resources：K8S资源限制

### alert-webhook

1. 通知服务，接收alertmanager推送的告警信息，再推送到企微或者钉钉。

2. 推送的内容为告警规则的：alertname、annotations的description和at。

kubectl apply -f 4.alert-webhook.yaml

* YAML文件注意事项：

* ALERTMANAGER_URL：alertmanager的外部访问URL，用于收到告警后可以点击进入告警屏蔽操作页面。

* DEFAULT_AT：当告警规则中没有配置annotations.at字段时，使用的默认@的人。

### grafana
* 展示告警数据的看板，请配置VM作为数据源，并导入K8S和Node的看板。

kubectl apply -f 5.grafana.yaml

* 看板：https://grafana.com/orgs/starsliao/dashboards

* YAML文件注意事项：

1. GF_SECURITY_ADMIN_USER: 登录账号设置

2. GF_SECURITY_ADMIN_PASSWORD: 登录密码设置

3. resources

* PV，PVC配置（当前使用本地主机存储，使用其它类型外部存储的请根据实际情况调整）

* 根据实际情况修改使用的storageClassName名称

* K8S资源限制

`storageClassName: local-path`

4. path: /k3s/data/grafana

* 本地主机存储的本地路径,需提前创建目录

5. nodeSelectorTerms

* 根据实际情况修改本地主机存储的节点名

6. storage

* 存储大小

### 告警规则

* 我的Grafana看板集合：

https://grafana.com/orgs/starsliao/dashboards



🔗 相关链接
https://mp.weixin.qq.com/s/K20YBZ7pIIEPcpRJx4Kg8A
https://github.com/starsliao/TenSunS



✨点击跳转：完整的K8S与主机告警规则

