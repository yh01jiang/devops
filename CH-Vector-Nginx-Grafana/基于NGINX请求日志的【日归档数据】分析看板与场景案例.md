# 🚀 基于NGINX请求日志的【日归档数据】分析看板与场景案例
## 📄 功能描述

* 基于已入库的Nginx日志，以日的维度，按域名聚合来分析业务请求数据。

* 每日每个域名聚合分析后仅一条数据入库，整体是一个非常轻量的数据表。

* 最终设计了一个看板来可视化这些聚合的数据，因为数据量少，就算一次查看几年的业务请求趋势数据都轻轻松松。

## 📌 场景分析
* 可以方便快捷的查看长期（多个月以及多年）的Nginx请求数据走势，观察业务的长期发展趋势，例如：基于去年同期活动数据，来对今年活动的所需资源提供比较与参考。

* 通过日级别的聚合数据，基于每日的统计数据，可以更清晰的发现业务的异常与短板，以及发布前后的数据对比，快速定位问题。

* 基于TOP排行榜，可以快速的发现异常的用户或请求，以及接口级别的业务异常佐证与明确业务请求重点优化方向。

##  💡案例回放

### 基于日归档的聚合数据分析，可以观察到日级别的业务异常与问题回溯。对隐形问题精准捕获。

* 520促销，数据库CPU100%导致系统响应延迟明显升高

<img width="1080" height="390" alt="image" src="https://github.com/user-attachments/assets/7925728a-c21d-443f-a390-1784869950f2" />


java微服务pod堆内存溢出，部分请求5XX突增

<img width="1080" height="394" alt="image" src="https://github.com/user-attachments/assets/3a253c5a-4c09-4e26-949a-02261eb02b9b" />


某次发布后，请求成功率降低了0.5%，观察到4xx请求数量级增长

<img width="1080" height="1246" alt="image" src="https://github.com/user-attachments/assets/38c2201b-4566-4743-9c3e-f47e7a179e47" />
<img width="1080" height="1246" alt="image" src="https://github.com/user-attachments/assets/911f1495-e79a-4844-91a8-581eabb8f29f" />


## 🎨 看板截图
* 每日高峰时段数据分析

<img width="1080" height="575" alt="image" src="https://github.com/user-attachments/assets/ecd2db9c-5d35-48a0-b351-03ee1472bd44" />
* 每日整体数据分析

<img width="1080" height="575" alt="image" src="https://github.com/user-attachments/assets/58cfc894-c6ad-4bb7-8ab9-a15b405f18da" />

* 每日整体异常请求数据排行榜

<img width="1080" height="608" alt="image" src="https://github.com/user-attachments/assets/fdf0c94f-2677-40f1-a8a0-02a13c46ac7f" />

* 每日整体用户请求数据排行榜


<img width="1080" height="608" alt="image" src="https://github.com/user-attachments/assets/e6f19e03-187a-4824-90e3-7516829e7757" />


## 🌈 核心功能

* **自动按日聚合**：日维度智能聚合nginx日志数据
* **高峰时段分析**：自动识别每天的业务高峰时段。
* **性能指标统计**：基于高峰时段统计QPS、响应时间、流量等关键指标
* **全天数据统计**：统计全天UV、PV、状态码分布、请求成功率
* **多维度分析**：支持按域名分组的详细分析
* T**OP排行榜**：生成IP、路径、慢路径、错误路径等多种TOP10排行榜
  
## 🎨  高峰时段指标
* 最大QPS、P99QPS
* 平均响应时间、P99响应时间、P90响应时间
* 响应时间分布与占比
* 最大请求带宽、最大响应带宽
  
## 全天统计指标
* 总UV(独立访客) 总PV(页面浏览量)
* HTTP状态码分布与占比
* 请求成功率
* 操作系统分布与占比

## 请求与异常的TOP排行榜
* 用户IP请求数TOP10
* URI请求数TOP10
* 最慢URI请求TOP10
* 用户IP访问URI最多TOP10
* 4xx错误URI TOP10
* 5xx错误URI TOP10

## 使用前提

#### 整体功能是基于：规范的Nginx日志已入库到ClickHouse作为前提的，详细请参考公众号合集：

云原生日志平台：采集、可视化分析、监控 全实践(第1篇)
https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzAwNzQ3MDIyMA==&action=getalbum&album_id=3669478369130889224#wechat_redirect

你还用ES存请求日志？CH+Vector打造最强Grafana日志分析看板
https://mp.weixin.qq.com/s?__biz=MzAwNzQ3MDIyMA==&mid=2247485456&idx=1&sn=1ed46f388d34041faae6ede651559fd1&scene=21#wechat_redirect

## 📖  K8S部署说明
本脚本采用K8S部署为一个CronJob的方式：每日凌晨读取Nginx日志库中前一天的数据，聚合后写入日归档的数据表中，通过Grafana看板实现可视化。

### 1. 新增CronJob
```bash
wget https://StarsL.cn/kubedoor/nginx-daily2ch-cronjob.yaml
# 注意：数据库连接配置修改为你之前存储NGINX日志的ClickHouse（使用CH的TCP端口9000）, 可以不填表名。
kubectl apply -f nginx-daily2ch-cronjob.yaml
```
### 2. 部署完成后请手动执行一次JOB进行初始化历史数据
kubectl create job -n default --from=cronjob/nginx-daily2ch nginx-daily2ch-init1

### 3. 导入Grafana看板，注意数据源要选择之前NGINX请求日志分析看板的数据源。
https://StarsL.cn/kubedoor/nginx-daily2ch-grafana.json

## 配置明细
#### 正常情况只需要修改ClickHouse数据库的配置即可。

如果您有更多的自定义配置：.env文件预置了所有的配置，修改部署yaml文件的env来配置：
**数据库连接配置：**

* CLICKHOUSE_HOST: ClickHouse服务器地址
* CLICKHOUSE_PORT: ClickHouse服务器端口（默认9000）
* CLICKHOUSE_DATABASE: 数据库名称（填写实时入库的nginx日志所在的库）
* CLICKHOUSE_TABLE:指定要分析的表名（为空时处理所有_access结尾的表(即默认写入ClickHouse的原始nginx日志表)）
* CLICKHOUSE_USER: 数据库用户名
* CLICKHOUSE_PASSWORD: 数据库密码

**表名配置**：

* SOURCE_TABLE_SUFFIX: Nginx实时入库的源表后缀（默认：_access）
* ARCHIVE_TABLE_SUFFIX: 日归档表后缀（默认：_archive_daily）

**时间周期配置：**

* PEAK_PERIOD_MINUTES:高峰时段分析的时间窗口，单位分钟（默认：30）
* QPS_CALCULATION_SECONDS:QPS计算的时间间隔，单位秒（默认：10）
* TRAFFIC_CALCULATION_SECONDS:流量统计的时间间隔，单位秒（默认：10）

**阈值配置：**

* MIN_DOMAIN_REQUESTS: 域名分析的最小请求次数阈值（默认：20）
* SLOW_PATH_MIN_REQUESTS:慢路径TOP10分析的最小请求次数阈值（默认：1000）

## 主机部署
```py
wget https://StarsL.cn/kubedoor/nginx-daily2ch.zip
# 编辑 .env文件，修改ClickHouse数据库配置
python3 main.py  #初始化历史数据
# 配置crontab 定时运行，每天凌晨采集前一天数据
30 0 * * * cd /opt/nginx-daily2ch && python3 main
```


## 脚本说明
```bash
# 默认模式（智能选择分析范围）
  # 当日归档表不存在时：会自动新建日归档表，然后执行全量分析（按日聚合除当天以外的全部历史数据）
# 如果日归档表已存在且有数据：执行增量分析（按日聚合昨天的数据）
# 自动删除重复日期数据，确保数据一致性，重复执行脚本无影响。
# 当 `CLICKHOUSE_TABLE` 为空时，脚本会自动发现并处理所有以 `_access` 结尾的表。
# 分析结果会自动存储到 ClickHouse 的日归档表中，表名格式为：`{原表名}_archive_daily`
python main.py

# 分析当天数据
python main.py --today

# 分析最近3天数据（不包括当天）
python main.py --recent 3

# 分析全部历史数据（不包括当天）
python main.py --all

```



