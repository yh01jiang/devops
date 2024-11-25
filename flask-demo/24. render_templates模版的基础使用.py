from flask import Flask,render_template,render_template_string

app = Flask(__name__,template_folder="templates")


@app.route("/")
def index():
    # index.html 就是templates模版下的index.html页面 
    # title="网页标题" 代表是键值对传参渲染到模版里面
    """ 单变量参数 """
    # return render_template("index.html", title="网页标题")
    """" 多变量参数 """
    title = "网页标题"
    context = "网页正文"
    html = render_template("index.html", **locals())
    print(html)  # 渲染后的html模版 
    return html


@app.route("/tmp")
def tmp():

    title = "网页标题"
    context = "网页正文"
    temp = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
</head>
<body>
    <!-- 渲染数据到html模版中 -->
    <h1>{{ context }}</h1>
</body>
</html>
"""
    html = render_template_string(temp, **locals())  
    print(html)  # 渲染后的html模版 
    return html

if __name__ == '__main__':
    app.run(debug=True)