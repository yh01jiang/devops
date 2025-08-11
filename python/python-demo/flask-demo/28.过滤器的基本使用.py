from flask import Flask,render_template

import random


app = Flask(__name__,template_folder="templates")

@app.route("/")
def index():
    # score = random.randint(1,100)
    # html = render_template("index2.html", **locals())

    book_list = [
        {"id": 1, "price": 78.50, "title": "js如门", "cover": "<img src='/static/images/course.png'>" ,},
        {"id": 2, "price": 78.5431,  "title": "python入门", "cover": "<img src='/static/images/course.png'>" ,},
        {"id": 3, "price": 66.66, "title": "vue入门", "cover": "<img src='/static/images/course.png'>" ,},
        {"id": 4, "price": 98.64, "title": "golang入门", "cover": "<img src='/static/images/course.png'>" ,},
    ]

    html = render_template("index5.html", **locals())
    print(html)
    return html



if __name__ == '__main__':
    app.run(debug=True)