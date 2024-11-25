from flask import Flask,render_template,session,g,url_for

app = Flask(__name__,template_folder="templates")

app.config["SECRET_KEY"] = "my secret key"

@app.route("/")
def index():
    # 基本类型
    num = 100
    num2 = 3.14
    is_bool = True
    title = "网页标题"


    # 复合类型
    set_var = {1, 2, 3, 4}
    list_var = ["小明", "小虎", "小黄"]
    dict_var = {"name": "root", "pwd": "123456"}
    touple_var = (1, 2, 3, 4)

    # 更复杂的数据结构
    book_list = [
        {"id": 10, "title": "图书馆标题10a", "description": "图书馆介绍", },
        {"id": 13, "title": "图书馆标题13b", "description": "图书馆介绍", },
        {"id": 21, "title": "图书馆标题21c", "description": "图书馆介绍", },
    ]

    session["uname"] = "root"
    g.num = 30

    html = render_template("index.html", **locals())
    print(html)
    return html

@app.route("/user/<uid>")  # /user/3
def user1(uid):
    return "ok"

@app.route("/user")  # /user?uid=3
def user2():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)