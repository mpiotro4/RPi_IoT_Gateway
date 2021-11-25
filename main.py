from flask import Flask
from flask.templating import render_template

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("index.jinja", message="Witaj świecie!")


@app.route("/nodes/create")
def create_node():
    return render_template("create_node.jinja")


@app.route("/nodes/show")
def show_nodes():
    return render_template("show_nodes.jinja")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
