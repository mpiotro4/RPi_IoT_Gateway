from flask import Flask
from flask.templating import render_template
from flask import request
import subprocess

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("index.jinja", message="Witaj świecie!")


@app.route("/nodes/create", methods=['GET', 'POST'])
def create_node():
    if request.method == 'GET':
        return render_template("create_node.jinja")
    if request.method == 'POST':
        proc = subprocess.Popen(
            ['python', 'dupa.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = proc.communicate()[0].decode()
        mac_address = request.form['mac_address']
        return render_template("create_node_summary.jinja", mac_address=output)


@app.route("/nodes/show")
def show_nodes():
    return render_template("show_nodes.jinja")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
