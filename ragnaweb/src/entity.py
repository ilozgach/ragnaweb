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
        self.web_auth_token = None
        self.web_auth_token_enabled = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def is_active(self):
        return True  # TODO: implement
    
    @property
    def is_authenticated(self):
        return True  # TODO: implement
    

    def get_id(self):
        return self.account_id
    
    

class Char(object):
    def __init__(self, **kwargs):
        self.char_id = None
        self.account_id = None
        self.char_num = None
        self.name = None
        setattr(self, "class", None)
        self.base_level = None
        self.job_level = None
        self.base_exp = None
        self.job_exp = None
        self.zeny = None
        self.str = None
        self.agi = None
        self.vit = None
        self.int = None
        self.dex = None
        self.luk = None
        self.max_hp = None
        self.hp = None
        self.max_sp = None
        self.sp = None
        self.status_point = None
        self.skill_point = None
        self.option = None
        self.karma = None
        self.manner = None
        self.party_id = None
        self.guild_id = None
        self.pet_id = None
        self.homun_id = None
        self.elemental_id = None
        self.hair = None
        self.hair_color = None
        self.clothes_color = None
        self.body = None
        self.weapon = None
        self.shield = None
        self.head_top = None
        self.head_mid = None
        self.head_bottom = None
        self.robe = None
        self.last_map = None
        self.last_x = None
        self.last_y = None
        self.save_map = None
        self.save_x = None
        self.save_y = None
        self.partner_id = None
        self.online = None
        self.father = None
        self.mother = None
        self.child = None
        self.fame = None
        self.rename = None
        self.delete_date = None
        self.moves = None
        self.unban_time = None
        self.font = None
        self.uniqueitem_counter = None
        self.sex = None
        self.hotkey_rowshift = None
        self.hotkey_rowshift2 = None
        self.clan_id = None
        self.last_login = None
        self.title_id = None
        self.show_equip = None

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __hash__(self):
        pass

    def to_dict(self):
        return {
            "char_id": self.char_id,
            "name": self.name
        }


class Mob(object):
    def __init__(self, **kwargs):
        self.mob_id = None
        self.sprite = None
        self.name = None

        for k, v in kwargs.items():
            setattr(self, k, v)