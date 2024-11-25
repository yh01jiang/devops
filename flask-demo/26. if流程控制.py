from flask import Flask,render_template

import random


app = Flask(__name__,template_folder="templates")

@app.route("/")
def index():
    score = random.randint(1,100)
    html = render_template("index2.html", **locals())

    print(html)
    return html



if __name__ == '__main__':
    app.run(debug=True)