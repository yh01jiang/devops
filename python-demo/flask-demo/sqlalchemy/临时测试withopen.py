import json

def demo(filename):
    with open(filename,mode='rt',encoding='utf-8') as f:
        data=json.load(f)
        print(data,type(data))

if __name__ == "__main__":
    demo(filename="/Users/jiangyuanhao/Desktop/project-demo/python-demo/flask-demo/sqlalchemy/1.json")


