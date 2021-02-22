import pymysql

import entity
import logger

log = logger.create()


class DbAccess(object):
    def __init__(self, host, user, passwd, db="ragnarok"):
        self.conn = pymysql.connect(host=host, user=user, password=passwd, database=db)

    def get_login_by_account_id(self, account_id):
        query = "SELECT * FROM login WHERE account_id={}".format(account_id)
        log.debug("Executing SQL query '{}'".format(query))
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()

        if len(data) == 0:
            log.debug("Query returned no data")
            return None

        login = entity.Login(**(data[0]))
        log.info("Query fetched login {{ {} }}".format(
            ", ".join("({} = {})".format(k, v) for k, v in login.__dict__.items() if type(k) is str)))
        return login

    def get_login_by_userid(self, userid):
        query = "SELECT * FROM login WHERE userid='{}'".format(userid)
        log.debug("Executing SQL query '{}'".format(query))
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()

        if len(data) == 0:
            log.debug("Query returned no data")
            return None

        login = entity.Login(**(data[0]))
        log.info("Query fetched login {{ {} }}".format(
            ", ".join("({} = {})".format(k, v) for k, v in login.__dict__.items() if type(k) is str)))
        return login

    def get_chars_by_account_id(self, account_id):
        query = "SELECT * FROM ragnarok.char WHERE account_id={}".format(account_id)
        log.debug("Executing SQL query '{}'".format(query))
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        cur.execute(query)
        data = cur.fetchall()

        if len(data) == 0:
            log.debug("Query returned no data")
            return []

        chars = []
        for d in data:
            char = entity.Char(**d)
            log.info("Query fetched char {{ {} }}".format(
                ", ".join("({} = {})".format(k, v) for k, v in char.__dict__.items() if type(k) is str)))
            chars.append(char)
        return chars
