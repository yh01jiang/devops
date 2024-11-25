from flask import Flask,session,request,make_response,redirect
app = Flask(__name__)

# 使用Session模块时就一定要配置SECRET_KEY全局  密钥
app.config["SECRET_KEY"] = "hfsojfaljfnfkanfkla"

@app.route("/set_session")
def set_session():
    """ session的设置  """
    # 设置session: session[‘name’]=’value’方法 
    session["username"] = "xiaoming"
    session["user_id"] = 21
    session["data"] = [1, 2, 3, 4, "AABC"]

    return "set_session"

@app.route("/get_session")
def get_session():
    """ session的读取  """
    print(f'username={session.get("username")}')
    print(f'user_id={session.get("user_id")}')
    print(f'data={session.get("data")}')
    return "get_session"


@app.route("/del_session")
def del_session():
    """ session的删除  """
    session.pop("username")
    session.pop("user_id")

    return "del_session"


""" 基于session实现传统网站登录的 """

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

    
    """ 接收客户端POST提交表单数据 """
    # 暂时不使用数据库，我们模拟用户身份判断代码
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "root" and password == "123456":
        """认证成功"""
        # 基于cookie保存登录状态，
        response = make_response("登录成功")
        session["username"] = "root"
        session["user_id"] = "root"
        return response
    else:
        """认证失败"""
        # 基于get请求的login 登录页面
        return redirect("/login")



@app.route("/user")
def user():
    """ 在部份需要认证身份的页面中，基于cookie判断用户的状态 """
    if not session.get("username"):
        return redirect("/login")
    
    else:
        return "个人中心信息展示"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)

