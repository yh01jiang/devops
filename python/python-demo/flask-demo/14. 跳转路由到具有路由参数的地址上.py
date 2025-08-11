from flask import Flask,redirect,url_for

app = Flask(__name__)

@app.route("/sms/<int:mobile>")
def sms(mobile):
    """ 发送短信 """
    return  f"发送短信到{mobile}"

@app.route("/info")
def info():
    # 跳转页面到一个具有路由参数的视图中
    # 这样写死了，因为我们大部分都只能知道视图名称
    # 方法1: 
    # return redirect("/sms/1332017865")

    # 方法2: 这种更灵活
    # url_for("视图名称"， “路由转换器参数”)===》 即使我们把/sms----》 改成/mobile ，也不影响函数的调用以及执行。
    url = url_for("sms", mobile=13312345678)
    print(url)  # /sms/13312345678
    return redirect(url)

    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)



# 在url_for中传参