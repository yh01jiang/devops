from flask import Flask
from werkzeug.routing.map import Map

"""
自定义路由转换器(在实际项目开发中,我们会单独准备一个python文件来保存转换器的定义代码)
"""
app = Flask(__name__)

app.config["DEBUG"] = True


from werkzeug.routing.converters import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, map, *args, **kwargs):
        super().__init__(map, *args, **kwargs)
        self.regex = args[0]

app.url_map.converters["regex"] = RegexConverter  # RegexConverter是类，在路由当中用regex别名代替他的，


@app.route("/sms/<regex('1[3-9]\d{9}'):mob_num>")
def sms(mob_num):
    return f"发送短信给手机号码: {mob_num}的用户"


@app.route("/goods/<regex('\d+'):id>")
def goods(id):
    return f"返回序列号为{id}的商品"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,)