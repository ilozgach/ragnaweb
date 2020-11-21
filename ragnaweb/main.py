import logging
import logging.config
import os
import settings

import yaml

log_cfg_file = os.path.join("logging.conf")
with open(log_cfg_file, "r") as f:
    log_cfg_data = yaml.load(f)
logging.config.dictConfig(log_cfg_data)

from flask import g, Flask, render_template, request, redirect
from flask_login.login_manager import LoginManager
from flask_login.utils import login_user, current_user
from db import DbAccess
from rodata import get_char_body_path, get_char_head_path

app = Flask(__name__)
login_manager = LoginManager()
app.config['SECRET_KEY'] = "secret_key"
login_manager.init_app(app)

log = logging.getLogger("main")

def get_db():
    if 'db' not in g:
        g.db = DbAccess(host=settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PASSWORD, db=settings.DB_NAME)
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
            # return render_template("char.html")
            return redirect("/chars")
        else:
            return render_template("login.html", fail_auth=True)
    else:
        return render_template("login.html", fail_auth=False)


@app.route("/chars", methods=['GET'])
def chars():
    RODATA = "d:/data"

    db = get_db()
    # chars = db.get_chars_by_account_id(current_user.account_id)
    chars = [0] * 15

    body_sprites = []
    body_actors = []
    head_sprites = []
    head_actors = []
    # for char in chars:
    #     spr_file = get_char_body_path(char, RODATA)
    #     if spr_file is not None:
    #         with open(unicode(spr_file), "rb") as f:
    #             d = f.read()
    #             d = map(ord, d)
    #             body_sprites.append(d)
    #         with open(unicode(spr_file.replace(".spr", ".act")), "rb") as f:
    #             d = f.read()
    #             d = map(ord, d)
    #             body_actors.append(d)
    #     else:
    #         body_sprites.append([])
    #         body_actors.append([])

    #     spr_file = get_char_head_path(char, RODATA)
    #     if spr_file is not None:
    #         with open(unicode(spr_file), "rb") as f:
    #             d = f.read()
    #             d = map(ord, d)
    #             head_sprites.append(d)
    #         with open(unicode(spr_file.replace(".spr", ".act")), "rb") as f:
    #             d = f.read()
    #             d = map(ord, d)
    #             head_actors.append(d)

    # return render_template("chars.html", chars=chars,
    #                        body_sprites=body_sprites, body_actors=body_actors,
    #                        head_sprites=head_sprites, head_actors=head_actors)

    return render_template("chars.html", chars=chars,
                           body_sprites=body_sprites, body_actors=body_actors,
                           head_sprites=head_sprites, head_actors=head_actors)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
