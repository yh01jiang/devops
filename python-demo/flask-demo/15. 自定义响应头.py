from flask import Flask,redirect,url_for

app = Flask(__name__)


@app.route("/")
def index():
    """ 自定义响应头 """
    return "hello ,flask", 201, {"company": "flask"}

    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)



# 自定义响应头