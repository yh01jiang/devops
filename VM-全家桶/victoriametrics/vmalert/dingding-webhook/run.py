# alert_to_dingtalk.py
import os
from flask import Flask, request, jsonify
from dingtalkchatbot.chatbot import DingtalkChatbot

app = Flask(__name__)

# # 从环境变量获取钉钉机器人配置
# DINGTALK_ACCESS_TOKEN = os.getenv('DINGTALK_ACCESS_TOKEN')
# DINGTALK_SECRET = os.getenv('DINGTALK_SECRET')  # 若启用加签则配置

# 硬编码
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=6**********875009"
DINGTALK_SECRET = "SEC840e8e73beb9************"  # 未启用加签则设为 None

def send_dingtalk_alert(alerts):
    bot = DingtalkChatbot(
        webhook=DINGTALK_WEBHOOK,
        secret=DINGTALK_SECRET
    )

    # bot.send_text(msg="flask人工触发消息哦")
    for alert in alerts:
        status = alert.get('status', 'firing')
        labels = alert.get('labels', {})
        annotations = alert.get('annotations', {})

        # 提取关键信息
        alertname = labels.get('alertname', 'Unknown Alert')  # type: ignore  # noqa
        instance = labels.get('instance', 'N/A')
        severity = labels.get('severity', 'warning')
        summary = annotations.get('summary', '')
        description = annotations.get('description', '')

        # 构建Markdown内容
        title = f"🚨 [{status.upper()}] {alertname}"
        text = (
            f"### {title}\n\n"
            f"- **实例**: `{instance}`\n"
            f"- **严重性**: {severity}\n"
            f"- **触发时间**: {alert.get('startsAt', '')}\n"
            f"- **摘要**: {summary}\n"
            f"---\n"
            f"{description}"
        )

        # 发送消息并处理@人员
        at_mobiles = [labels['at_mobile']] if 'at_mobile' in labels else None
        is_at_all = labels.get('at_all', 'false').lower() == 'true'

        try:
            bot.send_markdown(
                title=title[:50],  # 钉钉标题限制50字符
                text=text,
                at_mobiles=at_mobiles,
                is_at_all=is_at_all
            )
        except Exception as e:
            app.logger.error(f"钉钉消息发送失败: {str(e)}")
            raise


@app.route('/webhook', methods=['POST'])

def webhook():
    try:
        data = request.get_json()
        if not data or 'alerts' not in data:
            return jsonify({'status': 'invalid data'}), 400

        send_dingtalk_alert(data['alerts'])
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        app.logger.error(f"处理请求异常: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
