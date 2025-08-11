from flask import Flask
from flask import request

import json

from urllib.parse import parse_qs

app = Flask(__name__)

@app.route('/form',methods=["post"])
def form():
    """ 
    获取表单数据
    请求uri:

    """
    """获取客户端请求的请求体（表单）"""
    """获取表单数据[不包含上传文件]"""
    print(request.form)  # ImmutableMultiDict([('username', 'root'), ('password', '123456')])
    print(request.form["username"])    # root
    # 获取单个表单数据 
    print(request.form.get("username"))  # root
    # 获取多个表单数据
    print(request.form.getlist("fav"))  # ['swimming', 'shopping', 'drawin']

    """ 获取表单数据[包含上传文件] """
    print(request.form["username"])   
    print(request.files)  # ImmutableMultiDict([('file', <FileStorage: 'WechatIMG40.jpeg' ('image/jpeg')>)])
    print(request.files.get("file"))  # <FileStorage: 'WechatIMG14404 1.png' ('image/png')>
    print(request.files.getlist("file"))  # [<FileStorage: 'WechatIMG14404 1.png' ('image/png')>, <FileStorage: 'WechatIMG14404.png' ('image/png')>]


    return "hello flask"



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
