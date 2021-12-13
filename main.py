from flask import Flask
from flask.templating import render_template
from flask import request
import subprocess
import os.path
import sqlite3 as sql
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data_base.db")

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("index.jinja", message="Witaj świecie!")


@app.route("/nodes/create", methods=['GET', 'POST'])
def create_node():
    if request.method == 'GET':
        return render_template("create_node.jinja")
    if request.method == 'POST':
        # proc = subprocess.Popen(
        #     ['python3', f'/home/pi/ctl_wrapper/main.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # output = proc.communicate()[0].decode()
        output = "xd"
        name = 'no name'
        mac_address = request.form['mac_address']
        if(True):
            con = sql.connect(db_path)
            cur = con.cursor()
            cur.execute(f"""
                SELECT
                    node_id,
                    manufactured_node_id
                from manufactured_nodes
                WHERE mac_address = "{mac_address}"
            """)
            output = cur.fetchall()
            if not output:
                con.close()
                return render_template("create_node_summary.jinja", msg="Nie znaleziono węzła o podanym adresie MAC")
            else:
                cur.execute(f"""
                    INSERT INTO user_nodes (manufactured_node_id, node_id) VALUES('{output[0][1]}', '{output[0][0]}')
                """)
                con.commit()
                con.close()
                return render_template("create_node_summary.jinja", msg="Węzeł dodany pomyślnie")


@app.route("/nodes/read/<node_id>", methods=['GET'])
def read_node(node_id):
    if request.method == 'GET':
        con = sql.connect(db_path)
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute(f"""
        SELECT 
            user_node_id,
            name,
            mac_address,
            functions,
            direction,
            unit,
            description
        from user_nodes
        JOIN nodes USING (node_id)
        JOIN manufactured_nodes USING (manufactured_node_id)
        WHERE user_node_id = {node_id}
        """)
        row = cur.fetchall()
        cur.execute(
            f"""SELECT * from measurements WHERE user_node_id = {node_id} """)
        measurements = cur.fetchall()
        return render_template("read_node.jinja", node_id=node_id, row=row[0], measurements=measurements)


@app.route("/nodes/delete/<user_node_id>", methods=['DELETE'])
def delete_node(user_node_id):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute(
        f'DELETE FROM user_nodes WHERE `user_node_id` = {user_node_id}')
    con.commit()
    con.close()
    return f"Węzeł o id {user_node_id} usunięty pomyślnie"


@app.route("/nodes/show")
def show_nodes():
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("""
    SELECT 
        user_node_id,
        name,
        mac_address,
        functions
    from user_nodes
    JOIN nodes USING (node_id)
    JOIN manufactured_nodes USING (manufactured_node_id)
    """)
    rows = cur.fetchall()
    return render_template("show_nodes.jinja", rows=rows)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
