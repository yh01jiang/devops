# 1. 导入flask核心类
from flask import Flask

# 2. 初始化web应用程序实例化对象
app = Flask(__name__)

@app.route("/")

def hello():
    return "hello flask"
print(app.config)

