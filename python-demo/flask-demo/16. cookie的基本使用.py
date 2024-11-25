from flask import Flask,make_response, request,redirect
app = Flask(__name__)


@app.route("/set_cookie")
def set_cookie():
    """ cookie的设置  """
    # cookie保存客户端浏览器中，所以cookie必须跟着响应对象返回给客户端
    response = make_response("set_cookie")
    # response.set_cookie("变量名": "变量值",max_age="变量有效期")
    response.set_cookie("user_id", "100")  #  如果没有设置max_age，则当前cookie变量会在浏览器关闭（会话结束时被浏览器删除）
    response.set_cookie("username", "xiaoming", max_age=3600)  # 如果设置max_age,则按秒作为时间单位，设置cookie的有效时间
    response.set_cookie("num", "666", max_age=60) 
    return response

    

@app.route("/get_cookie")
def get_cookie():
    """ cookie的读取  """
    print("user_id=", request.cookies.get("user_id"))
    print("username", request.cookies.get("username"))
    return  "get_cookie"


@app.route("/del_cookie")
def del_cookie():
    """ cookie的删除  """
    response = make_response("del_cookie")
    response.set_cookie("user_id", "100", max_age=0)
    response.set_cookie("username", "xiaoming", max_age=0)
    return  response


""" 基于cookie实现传统网站登录的 """

@app.route("/login",methods=["post","get"])
def login():
    """ 基于cookie实现的登录"""
    form = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
        <form action="", method="post">
            账号: <input type="text", name="username"><br></br>
            密码: <input type="text", name="password"><br></br>
            按钮: <input type="submit", value="登录">
        </form>
    </body>

    </html>

    """
    # return make_response(form)
    if request.method == "GET":
        return make_response(form)
    # print(request.form)
    # return "ok"
    
    """ 接收客户端POST提交表单数据 """
    # 暂时不使用数据库，我们模拟用户身份判断代码
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "root" and password == "123456":
        """认证成功"""
        # 基于cookie保存登录状态，
        response = make_response("登录成功")
        response.set_cookie("username", username,max_age=7200)
        response.set_cookie("user_id", username,max_age=7200)
        return response
    else:
        """认证失败"""
        # 基于get请求的login 登录页面
        return redirect("/login")



@app.route("/user")
def user():
    """ 在部份需要认证身份的页面中，基于cookie判断用户的状态 """
    if not request.cookies.get("username"):
        return redirect("/login")
    
    else:
        return "个人中心信息展示"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)

