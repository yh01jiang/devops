VVG (Vector → VictoriaLogs → Grafana) 是一个高性能的日志收集、存储和可视化解决方案。

🏗️ 系统架构

┌─────────────────────┐    ┌──────────────────────┐     ┌─────────────────────┐
│                     │    │                      │     │                     │
│      Vector         │────│    VictoriaLogs      │──── │      Grafana        │
│   (日志收集器)       │    │     (日志存储)       │     │    (日志可视化)      │
│                     │    │                      │     │                    │
│  • Nginx 日志       │    │  • 高性能存储         │     │  • 查询界面         │
│  • Java 多行日志    │    │  • 数据压缩           │     │  • 仪表板           │
│  • 数据处理和转换    │    │  • 快速检索           │    │  • 告警功能          │
│                     │    │                      │    │                     │
└─────────────────────┘    └──────────────────────┘    └─────────────────────┘
         :8686                       :9428                       :3000

核心特性
🚀 高性能: VictoriaLogs 提供极高的写入和查询性能
📦 轻量级: 相比 ELK 栈，资源占用更少
🔧 易部署: Docker Compose 一键部署，vector支持kubernetes分布式部署
📊 可视化: Grafana 提供强大的日志查询和可视化功能
🔍 智能解析: 自动识别 Nginx 和 Java 日志格式
🔄 高可用: 支持多实例部署和负载均衡
📋 支持的日志格式
Nginx 日志
Access Log: 标准格式和 JSON 格式
Error Log: 标准错误日志格式
自定义格式: 支持自定义 log_format
Java 应用日志
单行日志: 标准 Java 应用日志
多行日志: 异常堆栈、调试信息自动合并 ⭐
智能识别: 支持时间戳和日志级别开头格式
双层处理: 容器运行时层 + 应用层多行处理 ⭐
JSON 格式: 结构化 Java 日志



## Vector 配置 - VVG 日志收集系统

```yaml
[root@cnsh-jump-server-prod conf]# cat nginx-victorlogs.yaml
############################################
# Vector 配置 - VVG 日志收集系统
# 支持 Nginx 和 Java 多行日志收集
############################################

api:
  enabled: true
  address: 0.0.0.0:8686

############################################################
# 1️⃣ Sources: 日志源配置
############################################################
sources:
  # Nginx Access 日志
  nginx_access:
    type: file
    #vector 可以递归收集/var/log/runtime/目录下所有路径的.log日志可以这么配置：- "/var/log/runtime/**/*.log"
    #include: ["/var/log/nginx/access.log"]
    include: ["/nginx_logs/access.log"]
    #ignore_older_secs: 86400          # 24h 无写入自动关闭句柄
    #max_read_bytes: 262144            # 单次 256 KiB
    #fingerprint:
    #  strategy: checksum
    #  important_bytes: 512


############################################################
# 2️⃣ Transforms: 日志解析和处理
############################################################
transforms:
  # Nginx Access 日志解析
  parse_access:
    type: remap
    inputs: [nginx_access]
    source: |
      # 保留原始行到 _msg，并删除 message 字段，避免重复存储
      msg = to_string!(.message)
      ._msg = msg
      del(.message)

      # --- ① 已是 JSON 的自定义 access 日志 -----------------
      if starts_with(msg, "{") {
        parsed, _ = parse_json(msg)        # 捕获错误到 _，不触发 E103
        if parsed != null {
          . |= merge!(., parsed)              # 将解析结果并入事件
        } else {
          .raw = msg                       # 留存无法解析的原文
        }

      }

      .log_type = "access"
      .service = "nginx"


############################################################
# 3️⃣ Sinks: 输出目标配置
############################################################
sinks:
  # 发送到 VictoriaLogs
  victorialogs:
    type: loki
    inputs: [parse_access]
    endpoint: http://172.29.36.107:9428
    path: /insert/loki/api/v1/push
    labels:
      job: "{{ service }}"
      log_type: "{{ log_type }}"
    encoding:
      codec: json               # 推送完整事件 JSON，包含 _msg
    request:
      concurrency: 4
      compression: gzip         # 启用gzip压缩，减少网络带宽
    healthcheck: false

  # 控制台输出（调试用）
  console:
    type: console
    inputs: [parse_access]
    target: stdout
    encoding:
      codec: text
      field: _msg
```

## grafana安装插件
victoriametrics-logs-datasource

<img width="1267" height="912" alt="image" src="https://github.com/user-attachments/assets/3997603f-70e1-4f9e-b2d7-3c24cf13d1d3" />


## grafana 查看日志
<img width="1867" height="941" alt="image" src="https://github.com/user-attachments/assets/2b810685-4e6a-41a9-bc6c-3e57f99b8757" />



# 参考链接：
https://github.com/seaworld008/vvg-logs-system/tree/main?tab=readme-ov-file#%EF%B8%8F-%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84
https://songxwn.com/Vector-VictoriaLogs-Grafana_Syslog/
