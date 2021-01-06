import logging
import logging.config
import os
import sys
current_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_folder, "src"))
import settings

import yaml
from datetime import timedelta

import flask_login
from flask import g, Flask, render_template, request, redirect, url_for
from flask_login.login_manager import LoginManager
from flask_login.utils import login_user, logout_user, current_user

import src.char_image_cache
import src.db
import src.logger
import src.renderer
import src.rodata

app = Flask(__name__)
login_manager = LoginManager()
app.config['SECRET_KEY'] = "secret_key"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(days=7)
login_manager.init_app(app)
log = src.logger.create()


def get_db():
    if 'db' not in g:
        g.db = src.db.DbAccess(host=settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PASSWORD, db=settings.DB_NAME)
    return g.db


def get_char_image_cache():
    if "char_image_cache" not in g:
        char_images_folder = os.path.join(current_folder, settings.CHAR_IMAGES_PATH)
        g.char_image_cache = src.char_image_cache.CharImageCache(base_path=char_images_folder)
    return g.char_image_cache


# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


@login_manager.user_loader
def load_user(account_id):
    db = get_db()
    login = db.get_login_by_account_id(account_id)
    return login


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # TODO: convert from unicode

        db = get_db()
        login = db.get_login_by_userid(username)

        if login is not None and login.user_pass == password:
            login_user(login, remember=True)
            return redirect("/chars")
        else:
            return render_template("login.html", fail_auth=True)
    else:
        return render_template("login.html", fail_auth=False)


@app.route("/logout", methods=['GET'])
def logout():
    if flask_login.current_user.is_authenticated:
        logout_user()
    return redirect(url_for("login"))


@app.route("/", methods=['GET'])
def default():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("chars"))
    return redirect(url_for("login"))



@app.route("/chars", methods=['GET'])
def chars():
    if not flask_login.current_user.is_authenticated:
        return redirect(url_for("login"))

    db = get_db()
    chars = db.get_chars_by_account_id(flask_login.current_user.account_id)
    char_image_cache = get_char_image_cache()
    rend = src.renderer.Renderer()
    for char in chars:
        if char not in char_image_cache:
            body_sprite_path = src.rodata.get_char_body_spr_path(char, settings.RODATA_PATH)
            head_sprite_path = src.rodata.get_char_head_spr_path(char, settings.RODATA_PATH)
            char_image_out_file_path = os.path.join(settings.CHAR_IMAGES_PATH, "{}.bmp".format(char.char_id))
            rend.render_char(body_sprite_path, head_sprite_path, char_image_out_file_path)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
