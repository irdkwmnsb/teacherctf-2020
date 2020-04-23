from layout import app
from flask import render_template, jsonify, request, abort, session, redirect, url_for
from layout.task import make_task, check_task


@app.route("/")
def index():
    if "cur_task" not in session:
        session["cur_task"] = make_task()
    if "done" not in session:
        session["done"] = 0
    if session["done"] >= app.config["TASKS_N"]:
        return render_template("flag.html")
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    ans = request.get_json()
    if not ans:
        return abort(400)
    if "cur_task" not in session:
        return redirect(url_for(index))
    test_res, test_msg = check_task(session["cur_task"], ans)
    if not test_res:
        return jsonify({"status": "wrong_answer", "msg": test_msg})
    del session["cur_task"]
    session["done"] += 1
    return jsonify({"status": "ok"})
