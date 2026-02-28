from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect("memo.db")
    conn.row_factory = sqlite3.Row
    return conn

# GET /api/memos
@app.route("/api/memos", methods=["GET"])
def api_get_memos():
    conn = get_db_connection()
    dataList = conn.execute(
        "SELECT * FROM memos ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return jsonify([dict(data) for data in dataList])

# POST /api/memos
@app.route("/api/memos", methods=["POST"])
def api_create_memo():
    data = request.json
    content = data.get("content")

    if not content:
        return jsonify({"error": "content is required"}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO memos (content) VALUES (?)",
        (content,)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "created"}), 201

# PUT /api/memos/<int:memo_id>
@app.route("/api/memos/<int:memo_id>", methods=["PUT"])
def api_update_memo(memo_id):
    data = request.json
    content = data.get("content")

    if not content:
        return jsonify({"error": "content is required"}), 400

    conn = get_db_connection()
    conn.execute(
        "UPDATE memos SET content = ? WHERE id = ?",
        (content, memo_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "updated"})

# DELETE /api/memos/<int:memo_id>
@app.route("/api/memos/<int:memo_id>", methods=["DELETE"])
def api_delete_memo(memo_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM memos WHERE id = ?",
        (memo_id,)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "deleted"})

def init_db():
    conn = sqlite3.connect("memo.db")

    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    with open(schema_path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)