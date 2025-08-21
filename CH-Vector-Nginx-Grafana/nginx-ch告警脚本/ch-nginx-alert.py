#!/usr/bin/python3
import time, requests, json
from clickhouse_driver import Client
from datetime import datetime, timedelta

# ClickHouse数据库连接信息
CK_HOST = "172.29.36.107"
CK_PORT = 9000  # ClickHouse TCP端口
CK_USER = "default"
CK_PASSWORD = ""
CK_DATABASE = "nginxlogs"  # ClickHouse nginx请求日志所在的数据库
tables = ["cassmall_hwprod_nginx_access", "smart_hwprod_nginx_access"]  # 存放access日志的表

# Alertmanager和告警相关配置
alertmanager_url = "http://主机:9095"  # Alertmanager地址
alarm_threshold = 10  # 5xx异常次数阈值
rt_threshold = 100  # RT延迟告警阀值(毫秒)
check_interval = 1  # 检查时间间隔(分钟)
group_token = '234a961429ba653638a2d90d***********************'  # 群机器人token

dingding_token = '234a961429ba653638a2d90d***********************'  # 群机器人token

## 企微应用推送的信息
corp_id = "wx34xxxxxx"  # 企微的公司corp_id
secret = "4kUHzGZghjltrWTpac"  # 企微应用的secret
agent_id = "1000011"  # 企微应用的agent_id
headers = {"content-type": "application/json"}
touser = "a1234|a6789"  # 企微的用户ID，支持同时推送多个用户，输入多个用户ID，并使用 | 分隔。

# 获取当前时间和检查时间段
now = datetime.now()
thism = now.strftime("%Y-%m-%d %H:%M")
beforem = (now - timedelta(minutes=check_interval)).strftime("%Y-%m-%d %H:%M")
tsthism = datetime.strptime(f"{thism}:00", "%Y-%m-%d %H:%M:%S").timestamp()
tsbeforem = datetime.strptime(f"{beforem}:00", "%Y-%m-%d %H:%M:%S").timestamp()
print(beforem, thism)

# 延迟告警的时间范围
timestart = datetime.strptime(str(now.date()) + '09:00', '%Y-%m-%d%H:%M')  # 开始时间
timeend = datetime.strptime(str(now.date()) + '18:00', '%Y-%m-%d%H:%M')  # 结束时间


# 获取企微token
def wb_token(current_timestamp):
    token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={secret}"
    response = requests.request("GET", token_url)
    token = response.json()['access_token']
    with open('token.pickle', 'wb') as file:
        pickle.dump([current_timestamp, token], file)
    return token

# 检查企微token
def get_token():
    current_timestamp = datetime.datetime.now().timestamp()
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as file:
            token_list = pickle.load(file)
            if current_timestamp - token_list[0] > 7000:
                print('获取新token')
                return wb_token(current_timestamp)
            else:
                print('使用旧token')
                return token_list[1]
    else:
        print('获取新token')
        return wb_token(current_timestamp)


def wecom_app(md, touser):
    token = get_token()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
    body = {
        "touser": touser,
        "msgtype": "markdown",
        "agentid": agent_id,
        "markdown": {"content": md},
    }
    r = requests.post(url=url, json=body, headers=headers)
    print(r.json())


def wecom_group(md, token, at=''):
    '''
    发送消息到企业微信
    at格式：
    - "@+企微ID"：@具体人；支持@多个人，写法：@abc@def
    - ""：不@人
    '''
    total_len = len(md.encode('utf-8'))
    if total_len > 4000:
        md = md[0:2000]  # 消息长度限制
    at = '<@' + '><@'.join(at.split('@')[1:]) + '>' if at else ''

    webhook = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={token}'
    headers = {'Content-Type': 'application/json'}
    params = {'msgtype': 'markdown', 'markdown': {'content': f"{md}\n{at}"}}
    data = bytes(json.dumps(params), 'utf-8')
    response = requests.post(webhook, headers=headers, data=data)
    print(f'【wecom】{response.json()}')


# 钉钉报警
def dingding(md,token):
    webhook = f'https://oapi.dingtalk.com/robot/send?access_token={token}'
    headers = {'Content-Type': 'application/json'}
    params = {"msgtype":"markdown","markdown":{"title":"告警通知","text":md},"at":{"isAtAll":True}}
    data = bytes(json.dumps(params), 'utf-8')
    response = requests.post(webhook, headers=headers, data=data)
    print(f'【dingding】{response.json()}')


# 飞书报警
def feishu(md,token):
    title = "告警通知"
    webhook = f'https://open.feishu.cn/open-apis/bot/v2/hook/{token}'
    headers = {'Content-Type': 'application/json'}
    params = {"msg_type": "interactive",
              "card": {"header": {"title": {"tag": "plain_text","content": title},"template": "red"},
                       "elements": [{"tag": "markdown","content": f"{md}\n<at id=all></at>",}]}}
    data = json.dumps(params)
    response = requests.post(webhook, headers=headers, data=data)
    print(f'【feishu】{response.json()}')


def is_silence(path):
    # 检查Alertmanager中是否有活跃的静默
    url = f"{alertmanager_url}/api/v2/silences?filter=type=%225xx%22&filter=path=%22{path}%22&active=true"
    silence_list = requests.get(url).json()
    sid_list = [i["id"] for i in silence_list if i["status"]["state"] == "active"]
    if sid_list:
        return True
    else:
        return False


# 连接ClickHouse数据库
ckclient = Client(host=CK_HOST, port=CK_PORT, user=CK_USER, password=CK_PASSWORD, database=CK_DATABASE)

for table in tables:
    # 查询5xx错误的请求
    query = f"""
        SELECT concat(domain,':',path) as path, responsetime, status, upstreamhost, server_ip, client_ip
        FROM {table}
        PREWHERE (timestamp >= '{beforem}:00' AND timestamp < '{thism}:00') AND (status > 499)
    """

    # 查询HTTP 200请求的平均响应时间
    rt_query = f"""
        SELECT avg(responsetime)
        FROM {table}
        PREWHERE (timestamp >= '{beforem}:00' AND timestamp < '{thism}:00') and (status=200)
    """

    result, _ = ckclient.execute(query, with_column_types=True)
    columns = [x[0] for x in _]
    rows = [dict(zip(columns, row)) for row in result]
    alert_url_dict = {}
    rowsnum = len(rows)
    print(f"{table}：5xx异常共计：", rowsnum)

    # 计算最近一分钟的HTTP 200平均响应时间
    try:
        rt = int(1000 * ckclient.execute(rt_query, with_column_types=False)[0][0])
    except:
        rt = 0
    print(f"{table}：最近1分钟HTTP200平均响应时间：", rt)
    if rt > rt_threshold and (now >= timestart and now <= timeend):
        rtmd = (
            f'## <font color="#ff0000">【{table}】</font>\n'
            f'- 最近1分钟HTTP200平均响应时间：<font color="#ff0000">{rt}ms</font>\n'
        )
        wecom_group(rtmd, group_token)
        # wecom_app(rtmd, touser)

    if rows:
        for row in rows:
            # 统计每个路径的异常信息
            if row["path"] not in alert_url_dict:
                alert_url_dict[row["path"]] = {}
            for column, value in row.items():
                if column == "path":
                    if "total" not in alert_url_dict[row["path"]]:
                        alert_url_dict[row["path"]]["total"] = 1
                    else:
                        alert_url_dict[row["path"]]["total"] += 1
                elif column == "responsetime":
                    if "responsetime" not in alert_url_dict[row["path"]]:
                        alert_url_dict[row["path"]]["responsetime"] = value
                    else:
                        alert_url_dict[row["path"]]["responsetime"] += value
                else:
                    if column not in alert_url_dict[row["path"]]:
                        alert_url_dict[row["path"]][column] = {}
                    if value not in alert_url_dict[row["path"]][column]:
                        alert_url_dict[row["path"]][column][value] = 1
                    else:
                        alert_url_dict[row["path"]][column][value] += 1
        # print(alert_url_dict)

        for k, v in alert_url_dict.items():
            if v["total"] >= alarm_threshold:
                url = k
                # 检查是否存在静默
                if is_silence(url):
                    print('===', url, '已被忽略')
                    continue
                print(f"==={table}：", url, "开始处理")
                urlnum = v["total"]
                # 查询特定路径的请求总数
                domain, path = url.split(':',1)
                url_query = f"""
                    SELECT count()
                    FROM {table}
                    PREWHERE (timestamp >= '{beforem}:00' AND timestamp < '{thism}:00') and domain = '{domain}' and path = '{path}'
                """
                count_url = ckclient.execute(url_query, with_column_types=False)[0][0]
                pnum = round(urlnum / count_url * 100, 2)
                responsetime = int(v["responsetime"] * 1000 / urlnum)

                # 生成告警信息
                nginxinfo = ""
                topnginx = sorted(v["server_ip"].items(), key=lambda x: x[1], reverse=True)
                for nginx, num in topnginx:
                    nginxinfo += f'{nginx}<font color="#ff0000">({num})</font>；'

                statusinfo = ""
                topstatus = sorted(v["status"].items(), key=lambda x: x[1], reverse=True)
                for status, num in topstatus:
                    statusinfo += f'{status}<font color="#ff0000">({num})</font>；'

                srcinfo = ""
                lensrc = "{:02d}".format(len(v["client_ip"]))
                top3src = sorted(v["client_ip"].items(), key=lambda x: x[1], reverse=True)[:3]
                for src, num in top3src[0:3]:
                    srcinfo += f'{src}<font color="#ff0000">({num})</font>\n                     '
                srcinfo = srcinfo.strip()

                destinfo = ""
                lendest = "{:02d}".format(len(v["upstreamhost"]))
                top3dest = sorted(v["upstreamhost"].items(), key=lambda x: x[1], reverse=True)[:3]
                for dest, num in top3dest[0:3]:
                    destinfo += f'{dest}<font color="#ff0000">({num})</font>\n                     '
                destinfo = destinfo.strip()

                silence_url = f"{alertmanager_url}/#/silences/new?filter=%7Btype%3D%225xx%22%2C%20path%3D%22{url}%22%7D"

                md = (
                    f'# {table}\n'
                    f'## <font color="#ff0000">【{url}】返回5XX异常 **{urlnum}** 次(耗时:{responsetime}ms,异常占:{pnum}%)</font>\n'
                    f"- 时间：{beforem}~~{thism}\n"
                    f"- 状态：{statusinfo}\n"
                    f"- NG：{nginxinfo}\n"
                    f"- 来源[3/{lensrc}]：{srcinfo}\n"
                    f"- 目标[3/{lendest}]：{destinfo}\n"
                    f"- [【屏蔽】]({silence_url})【当前时段总5XX：{rowsnum}】\n"
                )
                print(md)
                dingding(md, dingding_token)  # 修改为钉钉报警
                #wecom_group(md, group_token)
                # wecom_app(md, touser)
# 断开ClickHouse数据库连接
ckclient.disconnect()
