from flask import Flask,request,abort

app = Flask(__name__)

class NetWorkError(Exception):
    pass

@app.route("/")



def index():
    password = request.args.get("password")
    if password != "123456":
        """ 主动抛出异常 """
        # abort的第一个参数：表示本次抛出http异常状态码，后续其他参数，表示的就是错误相关的提示内容。
        # abort(400, "密码错误！！！")
        # print(hello)
        raise NetWorkError('网络请求错误')
        # raise Exception('错误错误了')  # 捕获不限类型的错误
    return "ok"


# @app.errorhandle 的参数是异常类型或者HTTP状态码
@app.errorhandler(NameError)
# 针对变量命名的异常处理 
def NameErrorFunc(exc, *args, **kwargs):
    print(dir(exc))
    print(exc.__traceback__)  # <traceback object at 0x101cb09c0>
    print(exc.code)
    print(exc.description)
    # return f"错误提示: {exc}"
    return {"error": f"错误提示: {exc}"} 



@app.errorhandler(400)
def error_400(exc):
    print(exc.__traceback__)  
    print(exc.code)         # 上面abort传递的错误状态码
    print(exc.description)  # 上面abort传递的错误描述
    return {"error": f"错误提示: {exc}"} 


@app.errorhandler(404)
def error_400(exc):
    print(exc.__traceback__)  
    print(exc.code)         # 上面abort传递的错误状态码
    print(exc.description)  # 上面abort传递的错误描述
    return {"error": "当前页面不存在"} 



@app.errorhandler(NetWorkError)
def network_error(exc):
    return {"error": f"{exc}"} 

if __name__ == '__main__':
    app.run(debug=True)