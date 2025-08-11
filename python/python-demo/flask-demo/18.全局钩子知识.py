from flask import Flask

app = Flask(__name__)
first_request = True  # 定义一个全局变量，初始值为 True

"""
# 2.3.0 版本之前的两个钩子函数
@app.before_first_request  但是在flask2.3.3 版本删除了app.before_first_request 装饰器）  2.3.0 版本之前可以使用的
app.before_first_request_funcs.append(before_first_request) 但是在flask2.3.3 版本删除了app.before_first_request 装饰器） 2.3.0 版本之前可以使用的

""" 

# @app.before_request
# def before_first_request():
""" 
    当项目启动之后，首次被客户端访问时自动执行 @app.before_request 所装饰的函数 （但是在flask2.3.3 版本删除了app.before_first_request 装饰器）
    用于项目初始化
    例如数据库的初始化、加载一些可以延后引入的全局配置
"""
#     global first_request  # 使用 global 关键字声明我们要使用全局变量
#     if first_request:  # 检查变量值
#         first_request = False  # 修改变量值，确保初始化操作只执行一次
#         # 执行一次性的初始化操作
#         print("在函数调用之前 before_first_request执行了！！！")

"""
# 代码执行流程
# 启动 Flask 应用：当 Flask 应用启动时，first_request 被初始化为 True。
# 第一次请求：
# 进入 before_request 钩子函数。
# global first_request 声明我们在这个函数中使用全局变量。
# 检查 first_request 的值：第一次请求时它是 True。
# 执行初始化操作（在这里是打印一条消息）。
# 将 first_request 设为 False，表示初始化操作已完成。
# 后续请求：
# 每次请求前都会调用 before_request 钩子函数。
# 由于 first_request 已经是 False，初始化操作不会再执行。
# 通过这种方式，我们确保初始化操作只在第一次请求时执行。希望这次解释更加清晰，让您理解如何使用全局变量和 global 关键字来实现这一功能。

"""

@app.before_request

def before_request():
    """
    每次客户端访问，视图执行之前，都会自动执行被 @app.before_request 所装饰的函数
    用于每次视图访问之前的公共逻辑代码的运行【身份验证 权限判断】
    """
    print("before_request执行了！！！")


@app.after_request

def after_request(response):
    """
    每次客户端访问，视图执行之后，都会自动执行被 @app.after_request 所装饰的函数
    用于每次视图访问之后的公共逻辑代码的运行（返回结果的加工、格式转换、日志记录）
    responce： 本次视图执行的响应对象
    """
    print("after_request执行了！！！！")
    # 自定义响应头
    response.headers["Content-Type"] = "application/json"
    response.headers["company"] = "flask.edu"
    return response

@app.teardown_request
def teardown_request(exc):
    """
    每次客户端访问，视图执行报错后，会自动执行 @app.teardown_request 所装饰的函数
    在flask2.2 之前 当debug=False，会自动执行 @app.teardown_request 所装饰的函数
    exc: 本次出现的异常实例对象
    """
    print("teardown_request执行了！！！")
    print(f"错误提示：{exc}")  # 异常提示

@app.route('/')

def hello():
    print("-------------第一个视图被执行了！！！----------------")
    # 1/0  # 测试上文的函数teardown_request 
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug= True)




