from flask import Flask, render_template, request
import json
import pathlib


app = Flask(__name__)


with open("config.json", "r") as cfg:
    cfg = json.loads(cfg.read())
    save_file = cfg.get("save_file")
save_data = []
if pathlib.Path(save_file).exists():
    with open(save_file, "r") as f:
        save_data = json.loads(f.read())


def save_to_file():
    with open(save_file, "w") as f:
        f.write(json.dumps(save_data))



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
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
        save_data.append(data)
        save_to_file()
        return "success"
    else:
        return "missing/invalid data"


if __name__ == '__main__':
    app.run("0.0.0.0", 80)
