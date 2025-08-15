1. 导入看板 (上文的json文件)
2. 新增 cronjob
注意修改为你之前存储NGINX日志的clickhouse的数据库信息, 不需要填表名.
```
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
            # ClickHouse数据库连接配置
            - name: CLICKHOUSE_HOST
              value: "10.7.0.102"
            - name: CLICKHOUSE_PORT
              value: "9000"
            - name: CLICKHOUSE_DATABASE
              value: "nginxlogs"
            - name: CLICKHOUSE_USER
              value: "default"
            - name: CLICKHOUSE_PASSWORD
              value: ""
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
```
kubectl create job --from=cronjob/nginx-daily2ch nginx-daily2ch-init1
