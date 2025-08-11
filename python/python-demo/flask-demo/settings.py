# DEBUG = True 

# def test(a:int, b:str):
#     # print(a, b)
#     print(a, type(a))
#     print(b, type(b))
#     return 1000

# if __name__ == '__main__':
#     test(1123, 'abc')
    



# num: int = 18
# print(num, type(num))




# num1 = 10
# print(num1, type(num1))



from flask import Flask

app = Flask(__name__)

from werkzeug.routing import BaseConverter

class MobileConverter(BaseConverter):
    regex = r'1[3-9]\d{9}'

app.url_map.converters["mobile"] = MobileConverter

@app.route("/sms/<mobile:mob_num>")
def sms(mob_num):
    return f"发送短信给手机号码: {mob_num}的用户"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,)