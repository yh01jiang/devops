# 1. 导入flask核心类
from flask import Flask

# 2. 初始化web应用程序实例化对象
app = Flask(__name__)

# 4. 可以通过实例化对象app提供的route装饰器，绑定视图与uri地址的关系
@app.route("/")
def hello_world():
    # 5. 默认flask支持函数式试图，视图的函数名不能重复，否则报错！！！
    # 视图的返回值将被flask包装成响应对象的HTML文档内容，返回给客户端。
    return "<h1>Hello, Flask!</h1>"



# 4. 可以通过实例化对象app提供的route装饰器，绑定视图与uri地址的关系

# 路由参数的传递
"""
<> 圈住,里面写上参数变量名
在视图中即可通过参数列表按命名来接收
接收参数时, 如果没有在路由中设置参数的类型, 则默认的参数类型时字符串类型
"""
@app.route("/goods/<cid>/<gid>")
def goods(cid, gid):
    print(cid, type(cid))
    print(gid,type(gid))
    return f"显示cid={cid} gid={gid}的商品信息"


if __name__ == '__main__':
    # 3. 运行flask提供的测试web服务器程序
    app.run(host='0.0.0.0', port=5000, debug=True)