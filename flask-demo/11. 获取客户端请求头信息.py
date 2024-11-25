from flask import Flask

from flask import request

app = Flask(__name__)

@app.route("/header", methods=["post","get","patch","delete", "put"])

def header():
    # 获取请求头其他信息
    print(request.headers, type(request.headers))  #  <class 'werkzeug.datastructures.headers.EnvironHeaders'>

    """获取单个请求头信息"""
    # 基于get使用请求头原始属性名获取    User-Agent 是客户端网络代理工具的名称
    print(request.headers.get("User-Agent"))  # PostmanRuntime/7.32.3
    # 把原始属性名转换成小写下划线格式来获取 
    print(request.user_agent)  # PostmanRuntime/7.32.3

    # 获取本次客户端的请求的服务器地址
    print(request.host)  # 127.0.0.1:5000

    # 获取本次客户端请求提交的数据格式
    print(request.content_type)  # multipart/form-data

    # 获取客户端请求的完整url路径
    print(request.url)  # http://127.0.0.1:5000/header

    # 获取客户端请求的服务端域名 
    print(request.root_url)  # http://127.0.0.1:5000/

    # 获取本次客户端请求的uri路径
    print(request.path)  # /header

    # 获取本次客户端的http请求方法
    print(request.method)  # POST

    # 获取本次客户端的ip地址
    print(request.remote_addr)  # 127.0.0.1

    # 获取本次客户端获取到服务端的信息
    print(request.server)  # ('0.0.0.0', 5000)

    # 获取本次客户端请求时，服务端系统的环境变量信息
    print(request.environ)  # {'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 'wsgi.input': <_io.BufferedReader name=5>, 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>, 'wsgi.multithread': True, 'wsgi.multiprocess': False, 'wsgi.run_once': False, 'werkzeug.socket': <socket.socket fd=5, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 5000), raddr=('127.0.0.1', 52666)>, 'SERVER_SOFTWARE': 'Werkzeug/3.0.3', 'REQUEST_METHOD': 'DELETE', 'SCRIPT_NAME': '', 'PATH_INFO': '/header', 'QUERY_STRING': '', 'REQUEST_URI': '/header', 'RAW_URI': '/header', 'REMOTE_ADDR': '127.0.0.1', 'REMOTE_PORT': 52666, 'SERVER_NAME': '0.0.0.0', 'SERVER_PORT': '5000', 'SERVER_PROTOCOL': 'HTTP/1.1', 'HTTP_USER_AGENT': 'PostmanRuntime/7.32.3', 'HTTP_ACCEPT': '*/*', 'HTTP_POSTMAN_TOKEN': '77356b31-a416-4298-b5ec-8cd14f7672fc', 'HTTP_HOST': '127.0.0.1:5000', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br', 'HTTP_CONNECTION': 'keep-alive', 'CONTENT_TYPE': 'multipart/form-data; boundary=--------------------------538157377667979761563685', 'CONTENT_LENGTH': '66752', 'werkzeug.request': <Request 'http://127.0.0.1:5000/header' [DELETE]>, 'werkzeug.debug.preserve_context': <built-in method append of list object at 0x103c49180>}

    """ 获取自定义请求头信息 """
    print(request.headers.get("fav"))  # test  因为自定义的header请求头是fav=test()


    print(request.data)

    return "hello flask"





if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000, debug=True)