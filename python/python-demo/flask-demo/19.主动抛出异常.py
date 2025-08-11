from flask import Flask,request,abort

app = Flask(__name__)

@app.route("/")

def index():
    password = request.args.get("password")
    if password != "123456":
        """ 主动抛出异常 """
        # abort的第一个参数：表示本次抛出http异常状态码，后续其他参数，表示的就是错误相关的提示内容。
        abort(403)
        print("x")
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)