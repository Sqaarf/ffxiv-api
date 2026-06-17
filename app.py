from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

SEAFOOD_DB_PATH = './data/seafood.db'
MINING_NODE_DB_PATH = './data/mining_node.db'

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/api/seafood", methods=["GET"])
def get_seafood():
    name = request.args.get("name")
    fishing_method = request.args.get("fishing_method")
    fishing_level = request.args.get("fishing_level")
    location = request.args.get("location")

    query = "SELECT name, icon, fishing_method, fishing_level, location, wiki_url FROM seafood WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")
    if fishing_method:
        query += " AND fishing_method = ?"
        params.append(fishing_method)
    if fishing_level:
        query += " AND fishing_level = ?"
        params.append(int(fishing_level))
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    con = sqlite3.connect(SEAFOOD_DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(query, params).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        con.close()

@app.route("/api/mining_node", methods=["GET"])
def get_mining_node():
    node_type = request.args.get("node_type")
    mining_level = request.args.get("mining_level")
    location = request.args.get("location")
    item = request.args.get("item")

    query = "SELECT node_type, mining_level, items, location FROM mining_node WHERE 1=1"
    params = []

    if node_type:
        query += " AND node_type = ?"
        params.append(node_type)
    if mining_level:
        query += " AND mining_level = ?"
        params.append(int(mining_level))
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")
    if item:
        query += " AND items LIKE ?"
        params.append(f"%{item}%")

    con = sqlite3.connect(MINING_NODE_DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(query, params).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        con.close()
