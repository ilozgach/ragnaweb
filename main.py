from flask import g, Flask, render_template, request
from flask_login.login_manager import LoginManager
from flask_login.utils import login_user
from auth import get_user, User
from db import DbAccess

app = Flask(__name__)
login_manager = LoginManager()
app.config['SECRET_KEY'] = "secret_key"
login_manager.init_app(app)


def get_db():
    if 'db' not in g:
        g.db = DbAccess(host="192.168.1.94", user="ragnarok", passwd="ragnarok", db="ragnarok")
    return g.db

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    login = db.get_login_by_id(user_id)
    return login


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # TODO: convert from unicode

        db = get_db()
        login = db.get_login_by_name(username)

        if login is not None and login.user_pass == password:
            login_user(login)
            return render_template("home.html")
        else:
            return render_template("login.html", fail_auth=True)
    else:
        return render_template("login.html", fail_auth=False)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
