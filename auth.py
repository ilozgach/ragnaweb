from flask_login.mixins import UserMixin


class User(UserMixin):
    def __init__(self, username, password, id, active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False


USERS = {
    "": User("", "", "0")
}


def get_user(username):
    return USERS.get(username, None)