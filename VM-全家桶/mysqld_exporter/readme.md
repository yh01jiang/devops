# 如何优雅的使用一个mysqld_exporter监控所有的MySQL实例
## 一、如何在TenSunS中接入云厂商的数据库
新增云账号的情况：目前新增时，支持多选区域，以及选择增加的资源类型，勾选MySQL即可接入自动同步云数据库，记得设置好同步间隔。
图片

对已经添加过的账号，增加同步云数据库资源：点击编辑云资源，选择好需要编辑的厂商、账号及区域，再勾选资源类型MySQL，配置上同步间隔即可增加自动同步云数据库。
图片

接入完成后，可手动点击同步按钮，完成首次同步；或者等待设定好的同步周期后会自动同步。
图片

同步完成后，可在云资源管理-MySQL管理-云MySQL列表，查看同步的云数据库信息。 图片
## 二、部署一个支持多实例的Mysqld_exporter
官方main版本的代码已经支持多目标的mysqld_exporter，只是还没有发Releases。所以基于最新的main版本自行编译了一个mysqld_exporter，并且做成了docker镜像。

详细说明查看：https://github.com/starsliao/multi_mysqld_exporter

新建一个docker-compose.yml，内容如下：

version: "3.2"
services:
  mysqld_exporter:
    image: swr.cn-south-1.myhuaweicloud.com/starsl.cn/mysqld_exporter:latest
    container_name: mysqld_exporter
    hostname: mysqld_exporter
    restart: always
    ports:
      - "9104:9104"
    volumes:
      - /usr/share/zoneinfo/PRC:/etc/localtime
    environment:
      MYSQLD_EXPORTER_PASSWORD: xxxxxxxxxxxxx
    entrypoint:
      - /bin/mysqld_exporter
      - --collect.info_schema.innodb_metrics
      - --collect.info_schema.tables
      - --collect.info_schema.processlist
      - --collect.info_schema.tables.databases=*
      - --mysqld.username=xxxxxxxxxx
      
docker-compose中有2个变量：监控专用的mysql账号和密码，注意修改掉后再启动。

docker-compose配置方式是所有的mysql实例都配置了一样的mysql监控账号和密码。

如果你有不同mysql实例需要配置不同监控账号密码的需求，请参考官方readme使用配置文件的方式启动。

🔗 相关链接: https://github.com/prometheus/mysqld_exporter

启动：docker-compose up -d

## 三、如何接入到Prometheus
点击菜单云资源管理-MySQL管理-prometheus配置 在右侧选择需要加入监控的云账号RDS组，并且输入mysqld_exporter的IP和端口，点击生成配置，即可复制生成的JOB内容到prometheus。 
<img width="1518" height="663" alt="image" src="https://github.com/user-attachments/assets/80ba27ca-32fc-4a75-949f-07660edfcd79" />


## 四、参考告警规则
<img width="1353" height="700" alt="image" src="https://github.com/user-attachments/assets/aac1ad60-4e5d-4376-960b-46a2884fd8bd" />


## 五、参考Grafana看板
GRAFANA：Mysqld Exporter Dashboard 22_11_01中文版

Grafana 看板详情： 
https://grafana.com/grafana/dashboards/17320
Grafana 看板ID：17320

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8affa95d-bef8-43ef-a7ef-3acd3b4e0097" />


<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/eae0fa0f-657e-4c45-b48b-568b19b08b2e" />






🔗 相关链接： 



https://github.com/starsliao/TenSunS/blob/main/docs/%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E7%9A%84%E4%BD%BF%E7%94%A8%E4%B8%80%E4%B8%AAmysqld_exporter%E7%9B%91%E6%8E%A7%E6%89%80%E6%9C%89%E7%9A%84MySQL%E5%AE%9E%E4%BE%8B.md




使用一个 mysqld exporter 监控所有的MySQL实例： https://blog.51cto.com/wutengfei/6030977
