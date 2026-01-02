from types import MethodType
import bcrypt
from flask import Flask, render_template, request
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)


def select_all_users():
    db = pymysql.connect(
        host="localhost",
        user="rusleak",
        passwd="pass",
        db="interdb"
    )
    cur = db.cursor()

    cur.execute("SELECT * FROM user")
    users = cur.fetchall()

    db.close()

    return users


# Вывод
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
            pass_from_bd = user[3]
            break

    if pass_from_bd is None:

        return render_template('login.html', error="User not found")


    if bcrypt.checkpw(password.encode(), pass_from_bd.encode()):
        return f"Login success: {username}"
    else:
        return render_template('login.html', error="Wrong password")


if __name__ == '__main__':
    app.run()
