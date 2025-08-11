from flask import Flask
from flask import request
import json

from urllib.parse import parse_qs

app = Flask(__name__)

@app.route('/data', methods=["post"])
def data():
    """ 
    获取表单数据
    请求uri:
    """
    """获取客户端是否是ajax请求获取本次客户端提交的数据格式是否是json, 返回的是true 或者false"""
    print(request.is_json)

    """ 获取客户端请求体中json数据 """
    print(request.json)  # {'username': 'json', 'password': '1123456'}
    print(request.json["username"])
    print(request.json.get("username")) 

    """ 获取请求体中原始数据"""
    print(request.data)  # b'{\n    "username": "json",\n    "password": "1123456"\n}'
    print(json.load(request.data))  #转为python对象  {'username': 'json', 'password': '1123456'}
    return "hello flask"

    """ 获取其他类型的数据 """
    print(request.data)

@app.route('/file', methods=["post", "put", "patch"])

def file():
    """ 接收上传文件并保存文件 """
    file = request.files.get("file")
    print(file) # <FileStorage: 'WechatIMG40.jpeg' ('image/jpeg')>
    # 调用FileStorage提供的save方法就可以保存文件了
    file.save("./demo1.png")
    return "hello flask"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


