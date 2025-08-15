# CH+Vector+Nginx打造最强Grafana日志分析

## 🚀 一、Nginx

### 1安装Nginx
```bash
yum install nginx -y （这里使用yum安装，推荐使用官方源安装）
systemctl start nginx
```

### 🔧 配置Nginx
```
编辑nginx.conf，增加以下配置
vim /etc/nginx/nginx.conf
    map "$time_iso8601 # $msec" $time_iso8601_ms { "~(^[^+]+)(\+[0-9:]+) # \d+\.(\d+)$" $1.$3$2; }
    log_format main
        '{"timestamp":"$time_iso8601_ms",'
        '"server_ip":"$server_addr",'
        '"remote_ip":"$remote_addr",'
        '"xff":"$http_x_forwarded_for",'
        '"remote_user":"$remote_user",'
        '"domain":"$host",'
        '"url":"$request_uri",'
        '"referer":"$http_referer",'
        '"upstreamtime":"$upstream_response_time",'
        '"responsetime":"$request_time",'
        '"request_method":"$request_method",'
        '"status":"$status",'
        '"response_length":"$bytes_sent",'
        '"request_length":"$request_length",'
        '"protocol":"$server_protocol",'
        '"upstreamhost":"$upstream_addr",'
        '"http_user_agent":"$http_user_agent"'
        '}';
    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';
    access_log  /var/log/nginx/access.log  main;
    ...
```

### 重载配置
```
systemctl start nginx
```


# 🚀 二、Docker以及docker-compose安装
```
## 💾 docker安装
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install -y yum-utils device-mapper-persistent-data lvm2
yum list docker-ce --showduplicates | sort -r
yum install -y docker-ce docker-ce-cli containerd.io
yum install docker-ce-23.0.3-1.el7 docker-ce-23.0.3-1.el7 containerd.io
systemctl start docker
systemctl enable docker


## 💾 docker-compose安装
https://github.com/docker/compose/releases
wget https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-linux-x86_64
docker-compose --version

 🔗 参考链接：https://www.cnblogs.com/yihuyuan/p/18773255


```

# 🚀 三、Clickhouse
### ⚙️ 1.创建部署目录和docker-compose.yaml
```
mkdir -p /opt/clickhouse/etc/clickhouse-server/{config.d,users.d}
cd /opt/clickhouse
cat <<-EOF > docker-compose.yaml
services:
  clickhouse:
    image: registry.cn-shenzhen.aliyuncs.com/starsl/clickhouse-server:23.4
    container_name: clickhouse
    hostname: clickhouse
    volumes:
      - /opt/clickhouse/logs:/var/log/clickhouse-server
      - /opt/clickhouse/data:/var/lib/clickhouse
      - /opt/clickhouse/etc/clickhouse-server/config.d/config.xml:/etc/clickhouse-server/config.d/config.xml
      - /opt/clickhouse/etc/clickhouse-server/users.d/users.xml:/etc/clickhouse-server/users.d/users.xml
      - /usr/share/zoneinfo/PRC:/etc/localtime
    ports:
      - 8123:8123
      - 9000:9000
EOF
```
⚙️ #### 配置主文件
```xml
vim /opt/clickhouse/etc/clickhouse-server/config.d/config.xml
<clickhouse replace="true">
    <logger>
        <level>debug</level>
        <log>/var/log/clickhouse-server/clickhouse-server.log</log>
        <errorlog>/var/log/clickhouse-server/clickhouse-server.err.log</errorlog>
        <size>1000M</size>
        <count>3</count>
    </logger>
    <display_name>ch_accesslog</display_name>
    <listen_host>0.0.0.0</listen_host>
    <http_port>8123</http_port>
    <tcp_port>9000</tcp_port>
    <user_directories>
        <users_xml>
            <path>users.xml</path>
        </users_xml>
        <local_directory>
            <path>/var/lib/clickhouse/access/</path>
        </local_directory>
    </user_directories>
</clickhouse>

```

⚙️ #### 配置用户文件
```xml
PASSWORD=$(base64 < /dev/urandom | head -c8); echo "$PASSWORD"; echo -n "$PASSWORD" | sha256sum | tr -d '-'
VGK7aP/z
40dc110052011b2663726f1794b9dabbf309077faf2d79d5ab4ae80b1cd9ccf7

vim /opt/clickhouse/etc/clickhouse-server/users.d/users.xml
<?xml version="1.0"?>
<clickhouse replace="true">
    <profiles>
        <default>
            <max_memory_usage>10000000000</max_memory_usage>
            <use_uncompressed_cache>0</use_uncompressed_cache>
            <load_balancing>in_order</load_balancing>
            <log_queries>1</log_queries>
        </default>
    </profiles>
    <users>
        <default>
            <password remove='1' />
            <password_sha256_hex>填写生成的密码密文{40dc110052011b2663726f1794b9dabbf309077faf2d79d5ab4ae80b1cd9ccf7}</password_sha256_hex>
            <access_management>1</access_management>
            <profile>default</profile>
            <networks>
                <ip>::/0</ip>
            </networks>
            <quota>default</quota>
            <access_management>1</access_management>
            <named_collection_control>1</named_collection_control>
            <show_named_collections>1</show_named_collections>
            <show_named_collections_secrets>1</show_named_collections_secrets>
        </default>
    </users>
    <quotas>
        <default>
            <interval>
                <duration>3600</duration>
                <queries>0</queries>
                <errors>0</errors>
                <result_rows>0</result_rows>
                <read_rows>0</read_rows>
                <execution_time>0</execution_time>
            </interval>
        </default>
    </quotas>
</clickhouse>

```
📦 启动
```
docker compose up -d
```

### 💾 2.创建数据库与表
#### 进入ck数据库
```
docker  exec -it clickhouse clickhouse-client --user default --password VGK7aP/z
```

#### ⚙️ 执行创建语句
```sql
CREATE DATABASE IF NOT EXISTS nginxlogs ENGINE=Atomic;

CREATE TABLE nginxlogs.nginx_access
(
    `timestamp` DateTime64(3, 'Asia/Shanghai'),
    `server_ip` String,
    `domain` String,
    `request_method` String,
    `status` Int32,
    `top_path` String,
    `path` String,
    `query` String,
    `protocol` String,
    `referer` String,
    `upstreamhost` String,
    `responsetime` Float32,
    `upstreamtime` Float32,
    `duration` Float32,
    `request_length` Int32,
    `response_length` Int32,
    `client_ip` String,
    `client_latitude` Float32,
    `client_longitude` Float32,
    `remote_user` String,
    `remote_ip` String,
    `xff` String,
    `client_city` String,
    `client_region` String,
    `client_country` String,
    `http_user_agent` String,
    `client_browser_family` String,
    `client_browser_major` String,
    `client_os_family` String,
    `client_os_major` String,
    `client_device_brand` String,
    `client_device_model` String,
    `createdtime` DateTime64(3, 'Asia/Shanghai')
)
ENGINE = MergeTree
PARTITION BY toYYYYMMDD(timestamp)
PRIMARY KEY (timestamp,
 server_ip,
 status,
 top_path,
 domain,
 upstreamhost,
 client_ip,
 remote_user,
 request_method,
 protocol,
 responsetime,
 upstreamtime,
 duration,
 request_length,
 response_length,
 path,
 referer,
 client_city,
 client_region,
 client_country,
 client_browser_family,
 client_browser_major,
 client_os_family,
 client_os_major,
 client_device_brand,
 client_device_model
)
TTL toDateTime(timestamp) + toIntervalDay(30)
SETTINGS index_granularity = 8192;

```

# 🚀 四、部署Vector采集日志
## Vector部署

```yaml
# 创建部署目录和docker-compose.yaml
mkdir -p /opt/vector/conf
cd /opt/vector
touch access_vector_error.log
wget https://raw.githubusercontent.com/P3TERX/GeoLite.mmdb/download/GeoLite2-City.mmdb
cat <<-EOF > docker-compose.yaml
services:
  vector:
    image: registry.cn-shenzhen.aliyuncs.com/starsl/vector:0.41.1-alpine
    container_name: vector
    hostname: vector
    restart: always
    entrypoint: vector --config-dir /etc/vector/conf 
    ports:
      - 8686:8686
    volumes:
      - /var/log/nginx:/nginx_logs  # 这是需要采集的日志的路径需要挂载到容器内
      - /opt/vector/access_vector_error.log:/tmp/access_vector_error.log
      - /opt/vector/GeoLite2-City.mmdb:/etc/vector/GeoLite2-City.mmdb
      - /opt/vector/conf:/etc/vector/conf
      - /usr/share/zoneinfo/PRC:/etc/localtime
EOF

```

### 🔧 Vector配置

```yaml
cd /opt/vector/conf
cat <<-EOF > vector.yaml
timezone: "Asia/Shanghai"
api:
  enabled: true
  address: "0.0.0.0:8686"
EOF


vim nginx-access.yaml
sources:
  01_file_nginx_access:
    type: file
    include:
      - /nginx_logs/access.log  #nginx请求日志路径，其实这里就算是vector 容器中的路径了。
transforms:
  02_parse_nginx_access:
    drop_on_error: true
    reroute_dropped: true
    type: remap
    inputs:
      - 01_file_nginx_access
    source: |
      .message = string!(.message)
      if contains(.message,"\\x") { .message = replace(.message, "\\x", "\\\\x") }
      . = parse_json!(.message)
      .createdtime = to_unix_timestamp(now(), unit: "milliseconds")
      .timestamp = to_unix_timestamp(parse_timestamp!(.timestamp , format: "%+"), unit: "milliseconds")
      .url_list = split!(.url, "?", 2)
      .path = .url_list[0]
      .query = .url_list[1]
      .path_list = split!(.path, "/", 3)
      if length(.path_list) > 2 {.top_path = join!(["/", .path_list[1]])} else {.top_path = "/"}
      .duration = round(((to_float(.responsetime) ?? 0) - (to_float(.upstreamtime) ?? 0)) ?? 0,3)
      if .xff == "-" { .xff = .remote_ip }
      .client_ip = split!(.xff, ",", 2)[0]
      .ua = parse_user_agent!(.http_user_agent , mode: "enriched")
      .client_browser_family = .ua.browser.family
      .client_browser_major = .ua.browser.major
      .client_os_family = .ua.os.family
      .client_os_major = .ua.os.major
      .client_device_brand = .ua.device.brand
      .client_device_model = .ua.device.model
      .geoip = get_enrichment_table_record("geoip_table", {"ip": .client_ip}) ?? {"city_name":"unknown","region_name":"unknown","country_name":"unknown"}
      .client_city = .geoip.city_name
      .client_region = .geoip.region_name
      .client_country = .geoip.country_name
      .client_latitude = .geoip.latitude
      .client_longitude = .geoip.longitude
      del(.path_list)
      del(.url_list)
      del(.ua)
      del(.geoip)
      del(.url)
sinks:
  03_ck_nginx_access:
    type: clickhouse
    inputs:
      - 02_parse_nginx_access
    endpoint: http://主机ip地址:8123  #clickhouse http接口
    database: nginxlogs  #clickhouse 库
    table: nginx_access  #clickhouse 表
    auth:
      strategy: basic
      user: default  #clickhouse 库
      password: GlWszBQp  #clickhouse 密码
    compression: gzip
  04_out_nginx_dropped:
    type: file
    inputs:
      - 02_parse_nginx_access.dropped
    path: /tmp/access_vector_error.log  #解析异常的日志
    encoding:
      codec: json
enrichment_tables:
  geoip_table:
    path: "/etc/vector/GeoLite2-City.mmdb"
    type: geoip
    locale: "zh-CN"

```

📦 启动: 运行Vector
docker compose up -d


# 🚀五、grafana

## 💾 docker部署grafana
```bash

mkdir data
docker run -d -p 3000:3000 --name=grafana \
  --user "$(id -u)" \  
  --volume "$PWD/data:/var/lib/grafana" \
  grafana/grafana-enterprise  

将要安装的插件作为逗号分隔列表传递给带有GF_INSTALL_PLUGINS环境变量的Docker
docker run -d -p 3000:3000 --name=grafana \
  -e "GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource" \  
  grafana/grafana-enterprise

```


## 💾 docker-compose部署grafana
```yaml
grafana:
  image: grafana/grafana:latest
  container_name: grafana
  ports:
    - "3000:3000"  # Grafana web UI端口
  volumes:
    - ./data/grafana:/var/lib/grafana  # 数据持久化存储
  environment:
    # 设置管理员admin用户的初始密码
    GF_SECURITY_ADMIN_PASSWORD: "admin"
    
    # 启用 Grafana 的 Explore 功能
    GF_EXPLORE_ENABLED: "true"
    
    # 安装 Grafana 插件
    GF_INSTALL_PLUGINS: "grafana-clock-panel,grafana-mqtt-datasource,tdengine-datasource,yesoreyeram-infinity-datasource"
    
    # 配置默认界面语言
    GF_VIEWER_LANGUAGE: "zh-Hans"
    
    # 启用匿名访问
    GF_AUTH_ANONYMOUS_ENABLED: "true"
    GF_AUTH_ANONYMOUS_ORG_ROLE: "Admin"  # 匿名用户角色设置
    
    # 允许嵌入 Grafana 面板到其他网页
    GF_SECURITY_ALLOW_EMBEDDING: "true"
    
    # 配置根 URL
    GF_SERVER_ROOT_URL: "http://${HOST}/grafana/home/"
    
    # 设置默认主题为 light
    GF_USERS_DEFAULT_THEME: "light"

##  🔧 安装ClickHouse插件
```
docker exec -it grfana bash
grafana cli plugins install grafana-clickhouse-datasource
docker restart grafana




## 增加数据源



导入看板





