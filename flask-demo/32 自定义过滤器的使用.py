from flask import Flask,render_template

from filters import do_fixed

app = Flask(__name__)

# 注册过滤器到当前应用实例对象
app.add_template_filter(do_fixed, "fixed")


# 第二种注册过滤器的方法

@app.template_filter("fixed2")
def do_fixed2(data):
    return f"{data:.2f}"


@app.route("/")

def index():
    return render_template('index10.html')


if __name__ == '__main__':
    app.run(debug=True)