from types import MethodType
import bcrypt
from flask import Flask, render_template, request
import pymysql
from flask import session, redirect, url_for

pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.secret_key = "very_secret_key"  # needed for sessions (simple demo key)
passwordb = "pass"

def select_all_users():
    db = pymysql.connect(
        host="localhost",
        user="rusleak",
        passwd=passwordb,
        db="interdb"
    )
    cur = db.cursor()

    cur.execute("SELECT * FROM user")
    users = cur.fetchall()

    db.close()

    return users


def register_user(username, password):
    db = pymysql.connect(
        host="localhost",
        user="rusleak",
        passwd=passwordb,
        db="interdb"
    )
    cur = db.cursor()

    # Проверка на дубликат сразу через SQL
    cur.execute("SELECT * FROM user WHERE email=%s", (username,))
    user = cur.fetchone()
    if user:
        db.close()
        return "User already exists"

    # Хешируем пароль
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cur.execute(
        "INSERT INTO user (email, password, role) VALUES (%s, %s, %s)",
        (username, password_hash, 'USER')
    )

    db.commit()
    db.close()
    return "OK"


# Show all
all_users = select_all_users()
for user in all_users:
    print(user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']

    all_users = select_all_users()
    pass_from_bd = None

    # ищем пользователя
    for user in all_users:
        if username == user[1]:
            pass_from_bd = user[2]
            break

    if pass_from_bd is None:

        return render_template('login.html', error="User not found")


    if bcrypt.checkpw(password.encode(), pass_from_bd.encode()):
        session['username'] = username   # remember who is logged in
        return redirect(url_for('myprofile'))
    else:
        return render_template('login.html', error="Wrong password")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form['username']
    password = request.form['password']

    result = register_user(username, password)

    if result == "User already exists":
        return render_template('register.html', error="User already exists")

    return render_template('register.html', success="User registered successfully")


@app.route('/myprofile')
def myprofile():
    # If not logged in: go to login page
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']

    # Get user info from database
    db = pymysql.connect(
        host="localhost",
        user="rusleak",
        passwd=passwordb,
        db="interdb"
    )
    cur = db.cursor()
    cur.execute("SELECT email, role FROM user WHERE email=%s", (username,))
    user = cur.fetchone()
    db.close()

    return render_template("myprofile.html", user=user)
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
