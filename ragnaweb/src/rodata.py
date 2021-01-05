MALE = u"³²"
FEMALE = u"¿©"
BODY_PATH_PREFIX = u"sprite/ÀÎ°£Á·/¸öÅë"
HEADS_PATH_PREFIX = u"sprite/ÀÎ°£Á·/¸Ó¸®Åë"

CLASS_TO_FILE_NAME = {
    0: (u"ÃÊº¸ÀÚ", "Novice"),
    6: (u"µµµÏ", "Thief"),
    4046: (u"ÅÂ±Ç¼Ò³â", "Taekwon"),
    4062: (u"·¹ÀÎÁ®", "Ranger")
}

def get_char_body_spr_path(char, rodata_path):
    cl = getattr(char, "class")
    sex = MALE if char.sex == "M" else FEMALE
    return u"/".join([rodata_path,
                     BODY_PATH_PREFIX,
                     sex,
                     "{}_{}.spr".format(JOB_TO_SPR_MAP[cl][0], sex)])


def get_char_head_spr_path(char, rodata_path):
    sex = MALE if char.sex == "M" else FEMALE
    return u"/".join([rodata_path,
                     HEADS_PATH_PREFIX,
                     sex,
                     u"{}_{}.spr".format(char.hair, sex)])
