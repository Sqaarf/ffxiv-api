from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

DB_PATH = './data/data.db'

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

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        rows = con.execute(query, params).fetchall()
        return jsonify([dict(row) for row in rows])
    finally:
        con.close()