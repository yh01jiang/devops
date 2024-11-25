from  flask import Flask,current_app,g

app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret key"


@app.route("/")
def index():
    # print(app)  # <Flask 'manage'>
    # print(current_app)  # current_app就是app应用实例对象在视图中的本地代理对象
    print(app is current_app)  # False
    print(app == current_app)  # true
    print(app.url_map)  #  <Rule '/' (GET, OPTIONS, HEAD) -> index>])
    print(current_app.url_map)  #  <Rule '/' (GET, OPTIONS, HEAD) -> index>])

    print(g)  # <flask.g of 'manage'>  # 全局数据存储对象，用于保存服务端存储的全局变量数据【可以理解为用户级别的全局变量存储对象】
    t1()
    t2()  # 可以拿到100这个数值
    return "ok"


def t1():
    # 存储数据
    g.user_id = 100

def t2():
    # 提取数据
    print(g.user_id)

if __name__ == '__main__':
    # print(request)  # 没有发生客户端请求时，调用request会超出请求上下文的使用范围
    print(app)  # <Flask 'manage'>
    # print(current_app) # 这样子获取不到的，如何获取到呢。
    with app.app_context():  # 相当于构建一个应用上下文环境
        print(current_app)
    app.run(debug=True)