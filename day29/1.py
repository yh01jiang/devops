
import os
import logging

receivers = {
    "Barry": {"files": ["1.txt", "2.txt"], "email": "barry.jiang@kerryprops.com"},
}


output_directory = "./"


for recipient_name, recipient_info in receivers.items():
    attachments = []
    for file in recipient_info["files"]:
        attachment_path = os.path.join(output_directory, file)
        if not os.path.exists(attachment_path):
            logging.error(f"文件 {attachment_path} 不存在,未发送邮件给 {recipient_name}")
            break
        else:
            attachments.append(attachment_path)