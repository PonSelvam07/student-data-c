from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'student.db'

def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS ST_ADM (
                EnrNo TEXT PRIMARY KEY,
                SName TEXT,
                Age INTEGER,
                Gender TEXT,
                Course TEXT,
                CFees REAL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM ST_ADM")
    students = cur.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            data = (
                request.form['enrno'],
                request.form['sname'],
                int(request.form['age']),
                request.form['gender'],
                request.form['course'],
                float(request.form['fees'])
            )
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("INSERT INTO ST_ADM VALUES (?, ?, ?, ?, ?, ?)", data)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error: {e}"
    return render_template('add.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
