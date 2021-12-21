from flask import Flask, redirect, url_for
from flask.templating import render_template
from flask import request
import subprocess
import os.path
import sqlite3 as sql
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data_base.db")
data_caputre_script_path = os.path.join(
    BASE_DIR, "data_capture_scripts/ctl_wrapper/main.py")
switch_script_patch = os.path.join(
    BASE_DIR, "data_capture_scripts/ctl_wrapper/switch.py")
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
        mac_address = request.form['mac_address']
        port = 1
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
                    INSERT INTO user_nodes (manufactured_node_id, node_id, port) VALUES('{output[0][1]}', '{output[0][0]}', {port})
                """)
                con.commit()
                con.close()
                return render_template("create_node_summary.jinja", msg="Węzeł dodany pomyślnie")


@app.route("/nodes/read/<user_node_id>", methods=['GET'])
def read_node(user_node_id):
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
            description,
            port
        from user_nodes
        JOIN nodes USING (node_id)
        JOIN manufactured_nodes USING (manufactured_node_id)
        WHERE user_node_id = {user_node_id}
        """)
        row = cur.fetchall()
        cur.execute(
            f"""SELECT * from measurements WHERE user_node_id = {user_node_id} """)
        measurements = cur.fetchall()
        functions = row[0]['functions'].split(',')
        return render_template("read_node.jinja", node_id=user_node_id, row=row[0], measurements=measurements, functions=functions)


@app.route("/nodes/delete/<user_node_id>", methods=['DELETE'])
def delete_node(user_node_id):
    con = sql.connect(db_path)
    cur = con.cursor()
    cur.execute(
        f'DELETE FROM user_nodes WHERE `user_node_id` = {user_node_id}')
    con.commit()
    cur.execute(
        f'DELETE FROM measurements WHERE `user_node_id` = {user_node_id}')
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


@app.route("/nodes/measure/<user_node_id>", methods=['GET'])
def capture_data(user_node_id):
    manufactured_node_id = db_select(
        f"""SELECT manufactured_node_id FROM user_nodes where user_node_id = '{user_node_id}'""")[0]['manufactured_node_id']
    mac_address = db_select(
        f"""SELECT mac_address FROM manufactured_nodes where manufactured_node_id = '{manufactured_node_id}' """)[0]['mac_address']
    proc = subprocess.Popen(
        ['python3', data_caputre_script_path, mac_address], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.communicate()[0].decode()
    db_insert(
        f"""insert into measurements (user_node_id, measure) values ('{user_node_id}', '{output}');""")
    return redirect(url_for('read_node', user_node_id=user_node_id))


@app.route("/nodes/switch/<user_node_id>/<mode>", methods=['GET'])
def switch(user_node_id, mode):
    manufactured_node_id = db_select(
        f"""SELECT manufactured_node_id FROM user_nodes where user_node_id = '{user_node_id}'""")[0]['manufactured_node_id']
    mac_address = db_select(
        f"""SELECT mac_address FROM manufactured_nodes where manufactured_node_id = '{manufactured_node_id}' """)[0]['mac_address']
    proc = subprocess.Popen(
        ['python3', switch_script_patch, mode], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return "jest git"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


def db_select(query):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute(query)
    return cur.fetchall()


def db_insert(query):
    con = sql.connect(db_path)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.executescript(query)
    return cur.fetchall()
