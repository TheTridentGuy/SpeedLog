from flask import Flask, render_template, request
import json
import pathlib


app = Flask(__name__)


with open("config.json", "r") as cfg:
    cfg = json.loads(cfg.read())
    save_file = cfg.get("save_file")
    port = cfg.get("port")
    address = cfg.get("address")
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


@app.route("/view")
def view():
    log_html = ""
    for entry in save_data:
        log_html += f"""<tr>
            <td><input type="checkbox" class="selcheck"></td>
            <td>{entry.get("callsign")}</td>
            <td>{entry.get("frequency")}</td>
            <td>{entry.get("date")}</td>
            <td>{entry.get("notes")}</td>
            <td>
                <button><div class="icon baseline"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M362.7 19.3L314.3 67.7 444.3 197.7l48.4-48.4c25-25 25-65.5 0-90.5L453.3 19.3c-25-25-65.5-25-90.5 0zm-71 71L58.6 323.5c-10.4 10.4-18 23.3-22.2 37.4L1 481.2C-1.5 489.7 .8 498.8 7 505s15.3 8.5 23.7 6.1l120.3-35.4c14.1-4.2 27-11.8 37.4-22.2L421.7 220.3 291.7 90.3z"/></svg></div></button>
                <button onclick="remove(this.parentElement.parentElement)"><div class="icon baseline"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg></div></button>
            </td>
        </tr>"""
    return render_template("viewer.html", entries=log_html)


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


@app.route("/dellog")
def dellog():
    index = request.values.get("index")
    if index:
        try:
            index = int(index)
        except TypeError:
            return "invalid json"
        print(index)
        save_data.pop(index)
        save_to_file()
        return "success"
    else:
        return "missing index parameter"


if __name__ == '__main__':
    app.run(address, port)  # set to 0.0.0.0 for production
