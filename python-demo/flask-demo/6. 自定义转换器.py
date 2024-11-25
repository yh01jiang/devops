from flask import Flask



# print('converters:', app.url_map.converters)



"""
自定义路由转换器(在实际项目开发中,我们会单独准备一个python文件来保存转换器的定义代码)
"""

# 第一步：导包 
# 自定转换器集成自werkzeug.routing中的BaseConverter类
from werkzeug.routing.converters import BaseConverter


app = Flask(__name__)

app.config["DEBUG"] = True

# 第二步：编写自定义函数
class MobileConverter(BaseConverter):
    """ 手机号参数类型的转换器 """
    regex = r"1[3-9]\d{9}"
    # pass
p
# 第三步：把自定义转换器添加到默认转换器中（DEFAULT_CONVERTERS）

app.url_map.converters["mobile"] = MobileConverter



@app.route("/sms/<mobile:mob_num>")
def sms(mob_num):
    return f"发送短信给手机号码: {mob_num}的用户"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,)