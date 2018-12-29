import MySQLdb
from flask import g


def connect_db():
    return MySQLdb.connect(host="192.168.1.94", user="ragnarok", passwd="ragnarok", db="ragnarok")


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


class Login(object):
    def __init__(self, **kwargs):
        self.account_id = None
        self.userid = None
        self.user_pass = None
        self.sex = None
        self.email = None
        self.group_id = None
        self.state = None
        self.unban_time = None
        self.expiration_time = None
        self.logincount = None
        self.lastlogin = None
        self.last_ip = None
        self.birthdate = None
        self.character_slots = None
        self.pincode = None
        self.pincode_change = None
        self.vip_time = None
        self.old_group = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def is_active(self):
        # TODO: implement
        return True

    def get_id(self):
        return unicode(str(self.account_id))


class DbAccess(object):
    def __init__(self, host, user, passwd, db="ragnarok"):
        self.conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)

    def get_login_by_id(self, id):
        id = int(id, 10)  # it should be always integer string

        query = "SELECT * FROM login WHERE account_id={}".format(id)
        cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()

        if len(data) == 0:
            return None

        return Login(**(data[0]))

    def get_login_by_name(self, name):
        query = "SELECT * FROM ragnarok.login WHERE userid='{}'".format(name)
        cur = self.conn.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()

        if len(data) == 0:
            return None

        return Login(**(data[0]))
