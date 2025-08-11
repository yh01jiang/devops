# from flask import Flask


# app = Flask(__name__)


# @app.route('/<any(student,class):url_path>/<id>/')
# def item(url_path, id):
#     if url_path == 'student':
#         return '学生{}详情'.format(id)
#     else:
#         return '班级{}详情'.format(id)
    


# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask,request


# app = Flask(__name__)

# @app.route('/student_name/')
# def school_name_list():
#     name = request.args.get('name')
#     age = request.args.get('age')
 
#     return "学生的姓名为{}，年龄为{}".format(name, age)
    


# if __name__ == '__main__':
#     app.run(debug=True)




# from flask import Flask,url_for
 
# app = Flask(__name__)
# app.config.update(DEBUG=True)
 
# @app.route('/')
# def demo1():
#     print(url_for("book"))  # 注意这个引用的是视图函数的名字 字符串格式
#     print(type(url_for("book")))
 
#     return url_for("book")
 
# @app.route('/book_list/')
# def book():
 
#     return 'flask_book'
 
# if __name__ ==  "__main__":
#     app.run()



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

@app.route("/demo")
def login():
    return "显示登录视图"



if __name__ ==  "__main__":
    app.run()
