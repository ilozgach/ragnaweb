import db
import settings

class TestDb():

    def setup_class(cls):
        cls.db_access = db.DbAccess(settings.DB_HOST,
                                    settings.DB_USER,
                                    settings.DB_PASSWORD,
                                    settings.DB_NAME)

    def test_get_login_by_account_id(self):
        login = self.db_access.get_login_by_account_id(2000000)
        assert login is not None
        assert login.userid == "ilozgach"

    def test_get_login_by_userid(self):
        login = self.db_access.get_login_by_userid("ilozgach")
        assert login is not None
        assert login.account_id == 2000000

    def test_get_chars_by_account_id(self):
        chars = self.db_access.get_chars_by_account_id(2000000)
        assert len(chars) == 1
        assert chars[0].name == "ZOHAN"
