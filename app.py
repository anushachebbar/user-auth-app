from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mysecretkey123'

# MySQL Configuration (we'll update these after Azure DB setup)
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = 'AmruthaC@2003'
app.config['MYSQL_DB']       = 'userdb'

mysql = MySQL(app)

# ─── HOME ───────────────────────────────────────────
@app.route('/')
def home():
    if 'username' in session:
        return render_template('dashboard.html', user=session['username'])
    return redirect(url_for('login'))

# ─── REGISTER ───────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing = cur.fetchone()

        if existing:
            msg = 'Email already registered!'
        else:
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            mysql.connection.commit()
            cur.close()
            msg = 'Registration successful! Please login.'
            return redirect(url_for('login'))
    return render_template('register.html', msg=msg)

# ─── LOGIN ──────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            msg = 'Invalid email or password!'
    return render_template('login.html', msg=msg)

# ─── LOGOUT ─────────────────────────────────────────
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)