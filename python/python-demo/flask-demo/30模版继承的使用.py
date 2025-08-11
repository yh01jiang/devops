from flask import Flask,render_template

import random


app = Flask(__name__,template_folder="templates")

@app.route("/")
def index():
    title = "站点首页"
    html = render_template("index7.html", **locals())
    return html


@app.route("/list")
def list():
    title = "商品列表页"
    html = render_template("index8.html", **locals())
    return html

@app.route("/user")
def user():
    title = "用户中心"
    html = render_template("index9.html", **locals())
    return html

if __name__ == '__main__':
    app.run(debug=True)