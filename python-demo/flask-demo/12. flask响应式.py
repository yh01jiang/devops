from flask import Flask,make_response,Response, jsonify
import json


app = Flask(__name__)

@app.route("/")

def index():
    """
    # 1. 接收客户端请求
    # 2. 根据客户端请求操作数据 文件
    # 3. 响应数据 操作结果
    """
    '''响应HTML文本，并设置响应状态码'''
    # 1. 直接返回元组(HTML文档，响应状态码)
    # return "<h1>hello, flask</h1>", 201

    # 2. 通过make_response返回Response 对象
    # response = make_response("<h1>hello, flask</h1>", 200)
    # print(response)  # <Response 21 bytes [200 OK]>
    # return response
    
    # 3. 通过Response 返回Response  对象
    # response = Response("<h1>hello, flask</h1>", 400)
    # return  response 
    # return Response("<h1>hello, flask</h1>", 400)


@app.route("/jsonapi")
def jsonapi():
    # """ 响应json数据 【原声写法】 """
    # data = {"name": "xiaoming", "age": 22}
    # return json.dumps(data), 200, {"Content-Type": "application/json"}

    """响应json数据 【jsonify】 """
    data = {"name": "xiaoming", "age": 22}
    return jsonify(data)


@app.route("/img")
def img():
    # 响应图片格式给客户端
    with open("./demo1.png", mode='rb') as f:
        data = f.read()
    return data, 200, {"Content-Type": "image/png"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)