import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging  # 引入 logging 模块


smtp_server = 'smtp.office365.com'
smtp_port = 587

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # 输出到控制台
        logging.FileHandler('/root/barry-oss-monitor-object/log/file.log')  # 输出到文件，请替换为你的日志文件路径
    ]
)

# 连接存储桶
auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
bucket = oss2.Bucket(auth, 'https://oss-cn-shanghai.aliyuncs.com', 'ack-oom-dump')


def load_last_scan_results(filename='/root/barry-oss-monitor-object/last_scan_results.json'):
    try:
         # 从文件中读取并解析JSON数据
        with open(filename, mode='rt') as f:
            last_scan_results = json.load(f)
        return last_scan_results
    except FileNotFoundError:
        # 如果文件不存在，则返回空字典
        return {}
    
# 将序列化的结果写入文件
def save_to_file(filename, data):
    with open(filename, mode='wt') as f:
        json.dump(data, f)

def scan_and_compare(bucket, last_scan_results={}):
    current_scan_results = {}

    # 列举Bucket下的所有文件
    for obj in oss2.ObjectIterator(bucket):
        current_scan_results[obj.key] = {'size': obj.size, 'etag': obj.etag}

    new_or_updated_files = []
    deleted_files = []


    for key in current_scan_results:
        # 检查新增或更新的文件
        if key not in last_scan_results:
            new_or_updated_files.append(key)
            continue
        # 检查文件是否有更新（ETag值不同）
        etag_in_current = current_scan_results[key]['etag']
        etag_in_last = last_scan_results.get(key, {}).get('etag')
        size_in_current = current_scan_results[key]['size']

        if (etag_in_current != etag_in_last) and (size_in_current > 0):
            new_or_updated_files.append(key)


    # 检查已删除的文件
    # for key in last_scan_results:
    #     if key not in current_scan_results:
    #         deleted_files.append(key)

    # 打印new_or_updated_files的内容
    for file in new_or_updated_files:
        print(file)

     # 打印current_scan_results的内容
    print("\nCurrent Scan Results:")
    for key, value in current_scan_results.items():
        print(f"Key: {key}, Size: {value['size']}, ETag: {value['etag']}")


    alert_files = []
    for f in new_or_updated_files:
        if current_scan_results[f]['size'] > 0:
            alert_files.append(f)


    if alert_files:
        send_alert_email(alert_files, "新增oom日志文件")
        # print("关于新增或更新的日志文件的告警邮件已发送成功")
        logging.info("关于新增或更新的日志文件的告警邮件已发送成功")

    # if deleted_files:
    #     send_alert_email(deleted_files, "删除7天之前的数据")
    #     # print("关于删除的日志文件的告警邮件已发送成功")
    #     logging.info("关于删除的日志文件的告警邮件已发送成功")

    return current_scan_results

def send_alert_email(files, describe):

    if files:
        base_url = "https://ack-oom-dump.oss-cn-shanghai.aliyuncs.com/"
        file_urls = []
        for file in files:
            full_url = base_url  + file
            file_urls.append(full_url)
        # 使用HTML将每个链接放在<li>标签中，并用<ul>包裹起来
        links_html = '<ul>\n'
        for url in file_urls:
            links_html += f'<li><a href="{url}">{url}</a></li>\n'
        links_html += '</ul>'
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    from_email = "tiservices.ml@kerryprops.com"
    email_password = 'K11ry2023(!)'  # 您的QQ邮箱应用密码 
    to_email  = "barry.jiang@kerryprops.com"
    # subject = f"OSS Storage Bucket File {status} Alert"
    subject= "主题: Java项目OSS发生OOM事件告警"
    # body = f"Hi All,<br/><br/>后端服务发生了OOM事件,请及时查看,<br/>{describe.capitalize()}files: {files} <br/> 文件链接: {', '.join(file_urls)}"
    body = f"Hi All,<br/><br/>后端服务发生了OOM事件,请及时查看,<br/>{describe.capitalize()}files: {files} <br/> 文件链接: <br/>\n{links_html}"
    
    cc_list = ["barry.jiang@kerryprops.com","deyang.gu@kerryprops.com","stone.pan@kerryprops.com"]
    #cc_list = ["barry.jiang@kerryprops.com",]
    msg = MIMEText(body, 'html')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Cc'] = ", ".join(cc_list)



    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(from_email, email_password)
    to_emails = [to_email] + cc_list

    server.sendmail(from_email, to_emails, msg.as_string())
    # print(f"邮件已成功发送至：{to_emails} 和抄送至 {', '.join(cc_list)}")
    logging.info(f"邮件已成功发送至：{to_emails} 和抄送至 {', '.join(cc_list)}")
    server.quit()

if __name__ == "__main__":
    last_scan_results = load_last_scan_results()
    current_scan_results = scan_and_compare(bucket, last_scan_results)
    save_to_file('/root/barry-oss-monitor-object/last_scan_results.json', current_scan_results)