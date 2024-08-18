from flask import Flask, render_template, request
import json


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def index():
    return render_template("about.html")


@app.route("/log")
def log():
    data = request.values.get("log")
    if data:
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return "invalid json"
        print(data)
        return "success"
    else:
        return "missing/invalid data"


if __name__ == '__main__':
    app.run("0.0.0.0", 80)
