from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'mysecretkey123'

# Dummy in-memory storage (for cloud demo)
users = {}

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

        if email in users:
            msg = 'Email already registered!'
        else:
            users[email] = {
                "username": username,
                "password": password
            }
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

        user = users.get(email)

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
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
