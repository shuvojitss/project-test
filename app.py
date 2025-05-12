from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ✅ Initialize database and table if not exists
def init_db():
    conn = sqlite3.connect('databaseer.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ✅ Home page with form
@app.route('/')
def form():
    return render_template('form.html')

# ✅ Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO submissions (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()

    return redirect('/records')

# ✅ Show all records page
@app.route('/records')
def records():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM submissions")
    records = c.fetchall()
    conn.close()
    return render_template('records.html', records=records)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
