from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)""")
conn.commit()
conn.close()

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

@app.route("/addnote", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/deletenote", methods=["POST"])
def delete_note():
    note_id = request.form["note_id"]
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/updatenote", methods=["POST"])
def update_note():
    note_id = request.form["note_id"]
    new_title = request.form["new_title"]
    new_content = request.form["new_content"]
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (new_title, new_content, note_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/clearnotes", methods=["POST"])
def clear_notes():
    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)