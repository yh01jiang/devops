# 🚀  基于K8S部署生产高可用的ES集群(附迁移方案)
## 🌈 ECK简介
https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-quickstart.html

🔗 相关链接: https://mp.weixin.qq.com/s?__biz=MzAwNzQ3MDIyMA==&mid=2247485407&idx=1&sn=49607c98662473de2cf3bd5fdbcac6bb&chksm=9b7cea3cac0b632a72ad4eda42eaae202da7e58dfd5b9a9417d4bbeb1c8cca0f2e50502c6c41&scene=178&cur_album_id=3669478369130889224&search_click_id=#rd

Elastic Cloud on Kubernetes (ECK) 是一个官方提供的用于在 Kubernetes 集群中简化部署、管理和操作 Elastic Stack（包括 Elasticsearch 和 Kibana）的扩展。

### ✨ ECK 是一个 Kubernetes Operator，它管理和自动化 Elastic Stack 的生命周期。通过使用 ECK，可以在 Kubernetes 环境中快速实现以下功能：

* 部署和管理 Elasticsearch 和 Kibana 实例，包括创建、删除、扩展和升级。

* 配置和调整 Elastic Stack 组件以满足特定需求。

* 自动处理故障检测、恢复和备份。

* 保护 Elasticsearch 集群，通过安全配置、证书管理和安全通信来确保数据安全。

* 监控 Elastic Stack 的性能和资源使用，从而优化集群性能。

## 🔧支持的版本
* Kubernetes 1.26-1.30（ECK2.14.0，低版本可以支持低版本的K8S，请自行到官网查看。）

* Elasticsearch, Kibana, APM Server: 6.8+, 7.1+, 8+

* Beats: 7.0+, 8+

* Logstash: 8.7+

## ⚙️ 部署 operator
```bash
kubectl create -f https://download.elastic.co/downloads/eck/2.14.0/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.14.0/operator.yaml
```
## 💾 部署 ES
**部署版本：**

* 7.17.24

**部署模式：**

* 3master节点，master，data共用节点。

* HTTP模式

* basic认证

* hostNetwork

* local-path

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: eslogs
  namespace: elastic-system
spec:
  version: 7.17.24
  http:
    tls:
      selfSignedCertificate:
        disabled: true
  nodeSets:
  - name: data
    count: 3
    podTemplate:
      spec:
        initContainers:
        - name: sysctl
          securityContext:
            privileged: true
            runAsUser: 0
          command: ['sh', '-c', 'sysctl -w vm.max_map_count=262144']
        containers:
        - name: elasticsearch
          env:
          - name: ES_JAVA_OPTS
            value: "-Xms16g -Xmx16g"
          resources:
            limits:
              cpu: 8
              memory: 32Gi
            requests:
              cpu: 500m
              memory: 512Mi
          volumeMounts:
          - name: timezone-volume
            mountPath: /etc/localtime
            readOnly: true
        volumes:
        - name: timezone-volume
          hostPath:
            path: /usr/share/zoneinfo/Asia/Shanghai
        affinity:
          podAntiAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
            - labelSelector:
                matchLabels:
                  elasticsearch.k8s.elastic.co/cluster-name: eslogs
              topologyKey: kubernetes.io/hostname
        hostNetwork: true
        dnsPolicy: ClusterFirstWithHostNet
    volumeClaimTemplates:
    - metadata:
        name: elasticsearch-data
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 3000Gi
        storageClassName: local-path
```
## 💾 部署Kibana
```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana
  namespace: elastic-system
spec:
  version: 7.17.24
  count: 3
  elasticsearchRef:
    # 对应上面ES资源的名称和命名空间
    name: eslogs
    namespace: elastic-system
  http:
    service:
      spec:
        type: NodePort
    tls:
      selfSignedCertificate:
        disabled: true
  podTemplate:
    spec:
      containers:
      - name: kibana
        env:
        - name: NODE_OPTIONS
          value: "--max-old-space-size=2048"
        - name: I18N_LOCALE
          value: zh-CN
        - name: SERVER_PUBLICBASEURL
          value: "http://log.xxxxxx.com"
        resources:
          requests:
            memory: 100Mi
            cpu: 0.5
          limits:
            memory: 4Gi
            cpu: 2
        volumeMounts:
        - name: timezone-volume
          mountPath: /etc/localtime
          readOnly: true
      volumes:
      - name: timezone-volume
        hostPath:
          path: /usr/share/zoneinfo/Asia/Shanghai
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                elasticsearch.k8s.elastic.co/name: kibana
            topologyKey: kubernetes.io/hostname
      hostNetwork: true
      dnsPolicy: ClusterFirstWithHostNet
```
## 💾 用户管理
```bash
# 解析: Secret: eslogs-es-elastic-user
# 获取elastic的密码
# 登录kibana在Stack Management,安全管理中进行用户管理
# http://10.1.0.26:5601/app/management/security/users
```
## 🌈 ES数据迁移
### 迁移方案: reindex
**设置索引模板，保证写入速率最大化**
```json
# 完成迁移后在索引管理中将number_of_replicas和refresh_interval参数设置为合适的值即可。
PUT _template/hwprod
{
  "index_patterns": [
    "hwprod*"
  ],
  "order": 999,
  "settings": {
    "refresh_interval": "-1",
    "number_of_shards": "3",
    "translog": {
      "sync_interval": "60s",
      "durability": "async"
    },
    "number_of_replicas": "0"
  }
}
```
### 配置集群白名单，新增源数据集群es地址
```bash
# 修改配置文件方式
vim /etc/elasticsearch/elasticsearch.yml 
reindex.remote.whitelist: "10.1.72.33:9200"
systemctl restart elasticsearch.service


# K8S部署增加环境变量方式
# 修改自定义资源的ES资源，增加环境变量
- name: ES_SETTING_REINDEX_REMOTE_WHITELIST
  value: 10.1.72.33:9200
```


### 执行reindex迁移
```json
# 请求
# size: 每批次的数据量
# slice: 切片数量, 和节点数一致
# wait_for_completion=false: 异步执行
POST _reindex?wait_for_completion=false
{
  "source": {
    "remote": {
      "host": "http://10.1.72.33:9200",
      "username": "elastic",
      "password": "asdf1234"
    },
    "index": "hwprod-2024.9.1",
    "size": 10000,
    "slice": {
      "id": 0,
      "max": 3
    }
  },
  "dest": {
    "index": "hwprod-2024.9.1"
  }
}

# 响应
{
  "task": "PuSABDEeTsSXUiW7U--uAw:40193"
}

# 查询异步任务
GET _tasks/PuSABDEeTsSXUiW7U--uAw:40193

```
