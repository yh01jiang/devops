from flask import Flask,request,redirect,url_for,Response

app = Flask(__name__)

@app.route("/user")
def index():
    if request.args.get("token"):
        return "显示个人中心"  
    # 跳转页面到登录视图中
    """ redirect("uri地址")  控制跳转页面到任意路径下"""
    # 方法1 
    # return redirect("/login")  

    # 方法2
    # 跳转页面到其他视图中（俗称：站内跳转） 
    url = url_for("login")  # url_for("视图名称")
    print(app.url_map)  # 路由列表，整个flask站点中的所有url地址和视图的映射关系都在这个属性里面
    print(url)  # /login
    return redirect(url)

@app.route("/login")
def login():
    return "显示登录视图"

@app.route("/jump")
def jump():
    """ 站外跳转 """
    ''' 
    301: 永久重定向，页面已经没有了，站点没有了，永久转移了。（域名映射---> 域名解析）
    302: 临时重定向，一般验证失败，访问需要权限的页面进行登录跳转时，都是属于临时跳转
    '''
    # 方法1: response = redirect("https://www.qq.com" ,302)
    # print(response)  # <Response 223 bytes [302 FOUND]> 发现这里是对象
    # return redirect("https://www.qq.com" ,302)

    # 底层原理 （redirect函数就是Response对象的页面跳转的封装）
    # 方法2: 
    res = Response('',302, {"Location": "https://www.163.com"})
    return res



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)