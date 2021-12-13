import sqlite3 as sql
import os.path
import random
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "data_base.db")

con = sql.connect(db_path)
con.row_factory = sql.Row
cur = con.cursor()
cur.execute(f"""
SELECT user_node_id FROM user_nodes
""")
user_nodes_ids = cur.fetchall()

for user_node_id in user_nodes_ids:
    print(user_node_id['user_node_id'])
    cur.executescript(
        f"""insert into measurements (user_node_id, measure) values ('{user_node_id['user_node_id']}', '{random.randint(20,30)}');""")
