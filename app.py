from flask import Flask, request, render_template, redirect, session, url_for, jsonify, abort, Response
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

myapp = Flask(__name__) 

myapp.config['MYSQL_HOST'] = 'localhost'
myapp.config['MYSQL_USER'] = 'flasku'
myapp.config['MYSQL_PASSWORD'] = 'flask123'
myapp.config['MYSQL_DB'] = 'flask'
myapp.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(myapp)


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6 , max=50)])
    password = PasswordField('Password', [validators.DataRequired(),validators.EqualTo('confirm', message = "Passwords do not match")])
    confirm = PasswordField('Confirm Password')

def add_user(name,email,username,password):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(name,email,username,password) VALUES (%s, %s, %s, %s)", (name,email,username,password))
    mysql.connection.commit()
    cur.close()


@myapp.route('/register', methods=['GET','POST'])
def register():
    if request.json is None:
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            name = form.name.data
            email = form.email.data
            username = form.username.data
            password = sha256_crypt.encrypt(str(form.password.data))
            add_user(name,email,username,password)
            return redirect(url_for('login'))

        return render_template('register.html',form=form)
    else:
        name = request.json['name']
        username = request.json['username']
        email = request.json['email']
        password = sha256_crypt.encrypt(str(request.json['password']))
        add_user(name,email,username,password)
        return jsonify({"status":"successful"})

def verify_user(username,password):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username = %s",[username])
    if result > 0:
        data = cur.fetchone()
        password_db = data["password"]
        if sha256_crypt.verify(password,password_db):
            session['logged_in'] = True
            session['username'] = username
            message = True
        else:
            message = False
    else:
        message = False
    cur.close()
    return message
            
@myapp.route('/login', methods=[ 'GET','POST'])
def login():
    if request.json is None:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            msg = verify_user(username, password)
            if msg:
                return redirect(url_for('home'))
            else:
                error = "Invalid Username or Password"
                return render_template('login.html')
        return render_template('login.html')
    else:
        username = request.json['username']
        password = request.json['password']
        msg = verify_user(username, password)
        if msg:
            return Response(status=200)
        else:
            abort(406)

@myapp.route('/')
def welcome():
    return render_template('welcome.html')

@myapp.route('/home')
@is_logged_in
def home():
    return render_template('home.html')

@myapp.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    myapp.secret_key = 'mysecret'
    myapp.run()  

