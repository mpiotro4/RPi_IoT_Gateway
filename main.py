from flask import Flask
from flask.templating import render_template
from flask import request
import subprocess
import os.path
import sqlite3 as sql

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "storage.db")

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
            ['python3', f'/home/pi/ctl_wrapper/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = proc.communicate()[0].decode()
        name = 'no name'
        mac_address = request.form['mac_address']
        if(True):
            try:
                with sql.connect(db_path) as con:
                    cur = con.cursor()
                    cur.execute(
                        f"INSERT INTO nodes VALUES(null, '{name }', '{mac_address}')"
                    )
                    con.commit()
                    con.close()
                    msg = "Record successfully added"
            except:
                con.rollback()
                msg = "error in insert operation"
            finally:
                return render_template("create_node_summary.jinja", output=output, msg=msg)


@app.route("/nodes/show")
def show_nodes():
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from nodes")
    rows = cur.fetchall()
    return render_template("show_nodes.jinja", rows=rows)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
