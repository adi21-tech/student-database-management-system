from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'gttc_secret_2025'

USERNAME = 'admin'
PASSWORD = 'gttc123'

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL,
        branch TEXT NOT NULL,
        year TEXT NOT NULL,
        marks REAL NOT NULL
    )''')
    conn.commit()
    conn.close()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html', error=None)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    search = request.args.get('search', '').strip()
    branch_filter = request.args.get('branch', '').strip()
    sort = request.args.get('sort', '')
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    query = 'SELECT * FROM students WHERE 1=1'
    params = []
    if search:
        query += ' AND (name LIKE ? OR roll_no LIKE ?)'
        params += [f'%{search}%', f'%{search}%']
    if branch_filter:
        query += ' AND branch LIKE ?'
        params.append(f'%{branch_filter}%')
    sort_map = {
        'name': 'name ASC',
        'roll_no': 'roll_no ASC',
        'year': 'year ASC',
        'marks': 'marks DESC'
    }
    if sort in sort_map:
        query += f' ORDER BY {sort_map[sort]}'
    c.execute(query, params)
    students = c.fetchall()
    conn.close()
    return render_template('index.html',
                           students=students,
                           search=search,
                           branch_filter=branch_filter,
                           sort=sort)

@app.route('/add', methods=['POST'])
@login_required
def add_student():
    name = request.form['name']
    roll_no = request.form['roll_no']
    branch = request.form['branch']
    year = request.form['year']
    marks = float(request.form['marks'])
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('INSERT INTO students (name, roll_no, branch, year, marks) VALUES (?, ?, ?, ?, ?)',
              (name, roll_no, branch, year, marks))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)