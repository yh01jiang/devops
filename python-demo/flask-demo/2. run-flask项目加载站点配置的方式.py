# 1. 导入flask核心类
from flask import Flask

# 2. 初始化web应用程序实例化对象
app = Flask(__name__)

"""第一种: flask项目加载站点配置方式 """
# app.config["配置项"] = 配置项的值
# app.config["DEBUG"] = True

""" 第二种: flask项目加载站点配置方式 """
# app.config 是整个flask项目默认的配置属性，里面包含了所有可用配置项，配置项的属性名都是大写字母或者大写字母+ 下划线
# config =  {
#     "DEBUG": True,
# }

# app.config.update(config)


# """第三种方式: 从配置文件加载配置"""
# import settings
# app.config.from_object("settings")


"第四种方式: 从类中去加载"
# class Config(object):
#     DEBUG = True
# app.config.from_object(Config)

""" 第五种： 从python文件去加载"""
# app.config.from_pyfile("settings.py")



"""第六种： 从环境变量中来配置 """
app.config.from_prefixed_env()
app.config["DEBUG"]   # 定义环境变量：export FLASK_DEBUG="True" ，加载变量去掉前缀
# app.config["SECRET_KEY"]
# 4. 可以通过实例化对象app提供的route装饰器，绑定视图与uri地址的关系
@app.route("/")
def hello_world():
    # 5. 默认flask支持函数式试图，视图的函数名不能重复，否则报错！！！
    # 视图的返回值将被flask包装成响应对象的HTML文档内容，返回给客户端。
    return "<h1>Hello, Flask!</h1>"



if __name__ == '__main__':
    print(app.config) # 配置都放在app.config, 可以简单理解为是一个字典，我们自然也可以通过直接修改它，app.config["键"] = 值
    # 3. 运行flask提供的测试web服务器程序
    app.run(host='0.0.0.0', port=5000)
    


# 参考文章：https://dormousehole.readthedocs.io/en/latest/config.html#id6
