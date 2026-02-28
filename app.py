from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("memo.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        memo = request.form.get("memo")

        if memo:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO memos (content) VALUES (?)",
                (memo,)
            )
            conn.commit()
            conn.close()

    conn = get_db_connection()
    dataList = conn.execute(
        "SELECT * FROM memos ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("index.html", dataList=dataList)

@app.route("/delete", methods=["POST"])
def delete():
    memo_id = request.form.get("id")

    if memo_id:
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM memos WHERE id = ?",
            (memo_id,)
        )
        conn.commit()
        conn.close()

    return redirect("/")

@app.route("/update", methods=["POST"])
def update():
    memo_id = request.form.get("id")
    content = request.form.get("content")

    if memo_id and content:
        conn = get_db_connection()
        conn.execute(
            "UPDATE memos SET content = ? WHERE id = ?",
            (content, memo_id)
        )
        conn.commit()
        conn.close()

    return redirect("/")

def init_db():
    conn = sqlite3.connect("memo.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True)