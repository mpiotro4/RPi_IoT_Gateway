import sqlite3
import os

# Remove a file

try:
    os.remove('data_base.db')
except:
    print("Error while deleting file ")


# create con object to connect
# the database geeks_db.db
con = sqlite3.connect("data_base.db")

# create the cursor object
cur = con.cursor()

# execute the script by creating the
# table named geeks_demo and insert the data
cur.executescript("""
    create table nodes(
        node_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        direction TEXT NOT NULL,
        functions TEXT NOT NULL
    );
   insert into nodes (name, direction, functions) values ( 'Węzeł testowy', 'Wyjścia', 'pomiar');
    """)

cur.executescript("""
    create table manufactured_nodes(
        manufactured_node_id INTEGER PRIMARY KEY,
        node_id INTEEGER NOT NULL,
        mac_address TEXT NOT NULL UNIQUE,
        pin TEXT NOT NULL
    );
    insert into manufactured_nodes (node_id, mac_address, pin) values ( '1', '00:20:12:08:B6:73', '1234');
    insert into manufactured_nodes (node_id, mac_address, pin) values ( '1', '00:00:00:00:00:00', '1234');
    """)

cur.executescript("""
    create table user_nodes(
        user_node_id INTEGER PRIMARY KEY,
        manufactured_node_id INTEEGER NOT NULL,
        node_id INTEEGER NOT NULL
    );
    insert into user_nodes (manufactured_node_id, node_id) values ('1', '1');
    insert into user_nodes (manufactured_node_id, node_id) values ('2', '1');
    """)

# display the data in the table by
# executing the cursor object
cur.execute("SELECT * from nodes")

# fetch all the data
print(cur.fetchall())


# display the data in the table by
# executing the cursor object
cur.execute("SELECT * from manufactured_nodes")

# fetch all the data
print(cur.fetchall())

# display the data in the table by
# executing the cursor object
cur.execute("SELECT * from user_nodes where node_id")
# fetch all the data
print(cur.fetchall())


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
print(cur.fetchall())

print("############")

cur.execute("""
    SELECT 
        node_id
    from manufactured_nodes
    WHERE mac_address = "00:00:00:00aasd:00:00"
    """)
print(cur.fetchall())
