from flask import Flask,render_template

app = Flask(__name__)

# 自定义过滤器
def do_mobile(data ,dot="*"):
    return data[:3] + dot*4 + data[-4:]

# 注册过滤器到当前应用实例对象
app.add_template_filter(do_mobile, "mobile")

@app.route("/")
def index():
    user_list = [
        {"id": 1,"name": "张三", "mobile": "13112345678",},
        {"id": 1,"name": "张三", "mobile": "13112345678",},
        {"id": 1,"name": "张三", "mobile": "13112345678",},
        {"id": 1,"name": "张三", "mobile": "13112345678",},
    ]

    html =  render_template('index11.html', **locals())
    return html


if __name__ == '__main__':
    app.run(debug=True)