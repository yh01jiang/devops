from flask import Flask,render_template

import random


app = Flask(__name__,template_folder="templates")

@app.route("/")
def index():
    # score = random.randint(1,100)
    # html = render_template("index2.html", **locals())

    book_list = [
        {"id": 10, "title": "图书馆标题10a", "description": "图书馆介绍", },
        {"id": 13, "title": "图书馆标题13b", "description": "图书馆介绍", },
        {"id": 21, "title": "图书馆标题21c", "description": "图书馆介绍", },
        {"id": 10, "title": "图书馆标题10a", "description": "图书馆介绍", },
        {"id": 13, "title": "图书馆标题13b", "description": "图书馆介绍", },
        {"id": 21, "title": "图书馆标题21c", "description": "图书馆介绍", },
        {"id": 10, "title": "图书馆标题10a", "description": "图书馆介绍", },
        {"id": 13, "title": "图书馆标题13b", "description": "图书馆介绍", },
        {"id": 21, "title": "图书馆标题21c", "description": "图书馆介绍", },
    ]

    data_list = [
        {"id": 1, "name": "小明", "sex": "1", },
        {"id": 2, "name": "小红", "sex": "0", },
        {"id": 3, "name": "小黑", "sex": "1", },
 
    
    ]

    html = render_template("index4.html", **locals())
    print(html)
    return html



if __name__ == '__main__':
    app.run(debug=True)