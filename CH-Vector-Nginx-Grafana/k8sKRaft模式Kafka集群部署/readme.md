# 🚀 扔掉Zookeeper！在K8S中运行KRaft模式Kafka集群

**从3.3.1开始，KRaft模式生产可用，使用KRaft模式的Kafka,不再需要维护Zookeeper。**

# 🔧 部署方案

* KRaft kafka on K8S的部署方案: Bitnami Kafka Helm chart
* https://github.com/bitnami/charts/tree/main/bitnami/kafka

## 💾  Helm Chart
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update bitnami 
helm search repo bitnami/kafka -l|more
# 本次安装kafka3.8.0版本
```
## ⚙️  修改配置与说明
```yaml
# vi kafka.yaml 
image:
  registry: registry.cn-shenzhen.aliyuncs.com
  repository: starsl/kafka #国内可使用仓库与镜像
  tag: 3.8
listeners:
  client:
    protocol: PLAINTEXT #关闭访问认证
  controller:
    protocol: PLAINTEXT #关闭访问认证
  interbroker:
    protocol: PLAINTEXT #关闭访问认证
  external:
    protocol: PLAINTEXT #关闭访问认证
controller:
  replicaCount: 3 #副本数
  controllerOnly: false #controller+broker共用模式
  heapOpts: -Xmx4096m -Xms2048m #KAFKA JVM
  resources:
    limits:
      cpu: 4 
      memory: 8Gi
    requests:
      cpu: 500m
      memory: 512Mi
  affinity: #仅部署在master节点,不限制可删除
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
          - matchExpressions:
              - key: node-role.kubernetes.io/master
                operator: Exists
          - matchExpressions:
              - key: node-role.kubernetes.io/control-plane
                operator: Exists
  tolerations: #仅部署在master节点,不限制可删除
    - operator: Exists
      effect: NoSchedule
    - operator: Exists
      effect: NoExecute
  persistence:
    storageClass: "local-path" #存储卷类型
    size: 100Gi #每个pod的存储大小
externalAccess:
  enabled: true #开启外部访问
  controller:
    service:
      type: NodePort #使用NodePort方式
      nodePorts:
        - 30091 #对外端口
        - 30092 #对外端口
        - 30093 #对外端口
      useHostIPs: true #使用宿主机IP
```
###  🥇 使用helm部署KAFKA
```bash
helm install kafka bitnami/kafka -f kafka.yaml --dry-run
helm install kafka bitnami/kafka -f kafka.yaml
```

## 📌 调用
### * K8S内部访问
```bash
kafka-controller-headless.default:9092

kafka-controller-0.kafka-controller-headless.default:9092
kafka-controller-1.kafka-controller-headless.default:9092
kafka-controller-2.kafka-controller-headless.default:9092
```

### * K8S外部访问
```bash
# node ip +设置的nodeport端口,注意端口对应的节点的ip
10.118.70.93:30091    
10.118.70.92:30092    
10.118.70.91:30093
# 从pod的配置中查找外部访问信息
kubectl exec -it kafka-controller-0 -- cat /opt/bitnami/kafka/config/server.properties | grep advertised.listeners
```

## 测试
### * 创建测试pod
```bash
kubectl run kafka-client --restart='Never' --image registry.cn-shenzhen.aliyuncs.com/starsl/kafka:3.8 --namespace default --command -- sleep infinity
```
### 生产消息
```bash
# 进入pod
kubectl exec --tty -i kafka-client --namespace default -- bash
kafka-console-producer.sh \
  --broker-list kafka-controller-0.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-1.kafka-controller-headless.default.svc.cluster.local:9092,kafka-controller-2.kafka-controller-headless.default.svc.cluster.local:9092 \
  --topic test
```
### 消费消息
```bash
# 进入pod
kubectl exec --tty -i kafka-client --namespace default -- bash
kafka-console-consumer.sh \
  --bootstrap-server kafka.default.svc.cluster.local:9092 \
  --topic test \
  --from-beginning
```

 🔗 ## 相关链接：https://mp.weixin.qq.com/s?__biz=MzAwNzQ3MDIyMA==&mid=2247485259&idx=1&sn=65e02cfb594384d8360a869d62995c63&chksm=9b7ceaa8ac0b63be35e7b52a0140126b4ff8a83a507b3a744e2f8572c0b0eb5ffe04856f9547&scene=178&cur_album_id=3669478369130889224&search_click_id=#rd
