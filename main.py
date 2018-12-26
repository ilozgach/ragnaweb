from flask import Flask, render_template, request
from flask_login.login_manager import LoginManager
from flask_login.utils import login_user
from auth import get_user

app = Flask(__name__)
login_manager = LoginManager()
app.config['SECRET_KEY'] = "secret_key"
login_manager.init_app(app)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user.password == password:
            login_user(user)
            return render_template("home.html")
        else:
            return render_template("login.html", fail_auth=True)
    else:
        return render_template("login.html", fail_auth=False)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
