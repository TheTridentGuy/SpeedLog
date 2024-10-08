"""
SpeedLog
Copyright (C) 2024  TheTridentGuy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from flask import Flask, render_template, request, redirect, session
import json
import pathlib
import secrets
import hashlib
import time


app = Flask(__name__)
app.secret_key = secrets.token_hex(64)
session_keys = {}


with open("config.json", "r") as cfg:
    cfg = json.loads(cfg.read())
    log_file = cfg.get("log_file")
    port = cfg.get("port")
    address = cfg.get("address")
    user_file = cfg.get("user_file")
    allow_acct_creation = cfg.get("allow_acct_creation")
if pathlib.Path(user_file).exists():
    with open(user_file, "r") as uf:
        user_data = json.loads(uf.read())
else:
    user_data = {}
save_data = {}
if pathlib.Path(log_file).exists():
    with open(log_file, "r") as f:
        save_data = json.loads(f.read())


def save_to_file():
    with open(log_file, "w") as f:
        f.write(json.dumps(save_data))


def verify_key(key):
    last_time = session_keys.get(key)
    if last_time:  # discard old session keys
        if (time.time() - last_time) < 600:
            session_keys[key] = time.time()
            return True
        else:
            del session_keys[key]
            return False
    else:
        return False


def add_user(username, password):
    with open(user_file, "w") as uf:
        user_data[username] = hashlib.sha512(password.encode("utf-8")).hexdigest()
        save_data[username] = []
        save_to_file()
        uf.write(json.dumps(user_data))


@app.route("/")
def index():
    key = session.get("key")
    if verify_key(key):
        return render_template("index.html")
    else:
        return redirect("/login?redirect=/")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/view")
def view():
    key = session.get("key")
    if verify_key(key):
        log_html = ""
        user_logs = save_data.get(session.get("username"))
        if user_logs:
            log_html = ""
            for entry in user_logs:
                log_html += f"""<tr>
                    <td><input type="checkbox" class="selcheck"></td>
                    <td>{entry.get("callsign")}</td>
                    <td>{entry.get("frequency") + ' ' + str(entry.get("unit"))}</td>
                    <td>{entry.get("date")}</td>
                    <td>{entry.get("notes")}</td>
                    <td>
                        <button onclick="remove(this.parentElement.parentElement)"><div class="icon baseline"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.6.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M135.2 17.7L128 32 32 32C14.3 32 0 46.3 0 64S14.3 96 32 96l384 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-96 0-7.2-14.3C307.4 6.8 296.3 0 284.2 0L163.8 0c-12.1 0-23.2 6.8-28.6 17.7zM416 128L32 128 53.2 467c1.6 25.3 22.6 45 47.9 45l245.8 0c25.3 0 46.3-19.7 47.9-45L416 128z"/></svg></div></button>
                    </td>
                </tr>"""
        return render_template("viewer.html", entries=log_html)
    else:
        return redirect("/login?redirect=/view")


@app.route("/log")
def log():
    key = session.get("key")
    if verify_key(key):
        data = request.values.get("log")
        if data:
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return "invalid json"
            print(data)
            save_data[session.get("username")].append(data)
            save_to_file()
            return "success"
        else:
            return "missing/invalid data"
    else:
        return redirect("/login?redirect=/")


@app.route("/dellog")
def dellog():
    key = session.get("key")
    if verify_key(key):
        index = request.values.get("index")
        if index:
            try:
                index = int(index)
            except TypeError:
                return "invalid json"
            print(index)
            save_data[session.get("username")].pop(index)
            save_to_file()
            return "success"
        else:
            return "missing index parameter"
    else:
        return redirect("/login?redirect=/view")


@app.route("/share")
def share():
    user_logs = save_data.get(request.values.get("user"))
    print(user_logs, request.values.get("user"))
    if isinstance(user_logs, list):
        log_html = ""
        for entry in user_logs:
            log_html += f"""<tr>
                    <td>{entry.get("callsign")}</td>
                    <td>{entry.get("frequency") + ' ' + str(entry.get("unit"))}</td>
                    <td>{entry.get("date")}</td>
                </tr>"""
        return render_template("share.html", entries=log_html, username=request.values.get("user"))
    elif session.get("username"):
        return redirect("/share?user="+session.get("username"))
    else:
        return render_template("message.html", header="User Error", body="")


@app.route("/export")
def export():
    key = session.get("key")
    if verify_key(key):
        if request.values.get("indexes") == "all":
            return save_data[session.get("username")]
        else:
            try:
                indexes = json.loads(request.values.get("indexes"))
                ret_data = []
                try:
                    username = session.get("username")
                    for index in indexes:
                        ret_data.append(save_data[username][index])
                except IndexError:
                    return "index error"
                return ret_data
            except json.JSONDecodeError:
                return "invalid indexes parameter"

    else:
        return redirect("/login?redirect=/view")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["redirect"] = request.values.get("redirect")
        return render_template("login.html")
    else:
        username = request.values.get("username")
        password = request.values.get("password")
        print(username, password)
        session["username"] = username
        if hashlib.sha512(password.encode("utf-8")).hexdigest() == user_data.get(username):
            new_key = secrets.token_hex(64)
            session["key"] = new_key
            session_keys[new_key] = time.time()
            if session.get("redirect"):
                return redirect(session.get("redirect"))
            else:
                return redirect("/")
        else:
            return render_template("loginerror.html")


@app.route("/createacct", methods=["GET", "POST"])
def createacct():
    if not allow_acct_creation:
        return render_template("message.html", header="Sorry, Account Creation is Disabled", body="")
    if request.method == "GET":
        return render_template("createacct.html")
    else:
        username = request.values.get("username")
        password = request.values.get("password")
        if save_data.get(username):
            return render_template("message.html", header="Sorry, that username is taken.", body="")
        print(username, password)
        add_user(username, password)
        return redirect("/login")


@app.route("/logout")
def logout():
    key = session.get("key")
    if key:
        del session_keys[key]
    return redirect("/login")


if __name__ == '__main__':
    app.run(address, port)
