# 1. 导入flask核心类
from flask import Flask,request

# 2. 初始化web应用程序实例化对象
app = Flask(__name__)

# 4. 可以通过实例化对象app提供的route装饰器，绑定视图与uri地址的关系
@app.route("/")
def hello_world():
    # 5. 默认flask支持函数式试图，视图的函数名不能重复，否则报错！！！
    # 视图的返回值将被flask包装成响应对象的HTML文档内容，返回给客户端。
    return "<h1>Hello, Flask!</h1>"



if __name__ == '__main__':
    # 3. 运行flask提供的测试web服务器程序
    app.run(host='0.0.0.0', port=5000, debug=True)



# 整个请求的处理过程如下所示：

# 当用户在浏览器地址栏访问这个地址，在这里即 http://127.0.0.1:5000/
# 服务器解析请求，发现请求 URL 匹配的 URL 规则是 /，因此调用对应的处理函数 hello_world()
# 获取 hello_world() 函数的返回值，处理后返回给客户端（浏览器）
# 浏览器接受响应，将其显示在窗口上