# 1. 导入flask核心类
from flask import Flask

# 2. 初始化web应用程序实例化对象
app = Flask(__name__)
# 开启DEBUG模式
app.config["DEBUG"] = True

# 4. 可以通过实例化对象app提供的route装饰器，绑定视图与uri地址的关系
# 参数1: rule设置当前视图的路由地址
# 参数2: methods设置当前视图的https请求方法，允许一个或多个方法，不区分大小写
@app.route(rule="/home", methods=["GET", "POST"])
def hello_world():
    # 5. 默认flask支持函数式试图，视图的函数名不能重复，否则报错！！！
    # 视图的返回值将被flask包装成响应对象的HTML文档内容，返回给客户端。
    return "<h1>Hello, Flask!</h1>"

"""路由和视图的名称必须全局唯一，不能出现重复，否则报错"""



if __name__ == '__main__':
    # 3. 运行flask提供的测试web服务器程序
    app.run(host='0.0.0.0', port=5000, )



# 什么是路由？

# 路由是一种映射关系，是绑定应用程序（视图）和url地址的一种 一对一的映射关系！我们在开发过程中，编写项目时所使用 路由往往是指代框架/项目
# 中用于完成路由功能的类，这个类一般是路由类，简称路由。



# 路由参数传递

