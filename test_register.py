# test_register.py
from flask import Flask, request, redirect, url_for, flash
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'dev-secret'
DATABASE = os.path.join(os.path.dirname(__file__), 'test_app.db')

def get_db_conn():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_table():
    conn = get_db_conn()
    conn.execute('''
      CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
      );
    ''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print('=== FORM DATA ===')
        print(request.form)   # >>> you will see this in the terminal
        username = request.form.get('username','').strip()
        email = request.form.get('email','').strip()
        password = request.form.get('password','').strip()

        if not username or not email or not password:
            flash('Fill all fields')
            return redirect(url_for('register'))

        try:
            conn = get_db_conn()
            cur = conn.cursor()
            cur.execute("INSERT INTO patients (username, email, password) VALUES (?, ?, ?)",
                        (username, email, password))
            conn.commit()
            conn.close()
            flash('Registered!')
            return redirect(url_for('register'))
        except Exception as e:
            print('DB ERROR:', e)
            flash('Server error (see terminal)')
            return redirect(url_for('register'))

    # simple page shown when visiting in browser
    return '''
    <!doctype html><html><body>
    <h1>Register</h1>
    <form method="post" action="/register">
      <label>Username <input name="username" type="text" required></label><br>
      <label>Email    <input name="email" type="email" required></label><br>
      <label>Password <input name="password" type="password" required></label><br>
      <button type="submit">Register</button>
    </form>
    </body></html>
    '''

if __name__ == '__main__':
    ensure_table()
    app.run(debug=True)
