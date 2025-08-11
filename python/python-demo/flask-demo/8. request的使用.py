from flask import Flask
from flask import request

from urllib.parse import parse_qs

app = Flask(__name__)

@app.route('/qs')
def qs():
    # print(request, type(request))  # 获取本次客户端的请求对象
   

    """获取客户端请求的查询字符串参数"""

    """ 请求uri地址: http://127.0.0.1:5000/qs?username=xiaoming&age=18"""
    # 方法1: 获取原始查询字符串参数，格式为bytes
    # print(request.query_string)  # b'username=xiaoming&age=18'

    # 1） 针对原始的查询字符串参数，转换为字典格式
    query_string = parse_qs(request.query_string.decode())
    print(query_string)

    # 获取参数值
    print(query_string["username"][0])


    # 方法2: 获取原始查询字符串参数，格式为ImmutableMultiDict
    print(request.args)  # ImmutableMultiDict([('username', 'xiaoming'), ('age', '18')])

    # 2) 获取单个参数值
    # print(request.args["username"])
    # print(request.args["age"])

    # 3) 获取多个参数值
    print(request.args["username"])  # xiaoming 
    print(request.args["fav"])       # shopping


    print(request.args.get("username")) # xiaoming

    print(request.args.getlist("fav"))  # ['shopping', 'coding', 'rap']

    print(request.args.getlist("fav")[0])  # shopping
    return "hello flask"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
