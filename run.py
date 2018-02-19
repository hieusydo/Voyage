# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__, static_folder="static", template_folder="templates")

app.config['TEMPLATES_AUTO_RELOAD'] = True
# url_for('static', filename='style.css')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/view")
def view():
    return render_template("view.html")

@app.route("/logout")
def logout():
    return render_template("logout.html")

if __name__ == "__main__":
    app.run(debug=True)