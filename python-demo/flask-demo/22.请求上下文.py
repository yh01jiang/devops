from  flask import Flask,request,session

app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret key"


def test():
    print(request)  # 请求上下文所提供的对象[request或者session]，只能被视图直接或者间接调用

@app.route("/")
def index():
    print(request)
    print(session)
    test()
    return "ok"


if __name__ == '__main__':
    # print(request)  # 没有发生客户端请求时，调用request会超出请求上下文的使用范围
    app.run(debug=True)