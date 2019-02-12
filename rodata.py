# -*- coding: utf-8 -*

# import os

MALE = u"³²"
FEMALE = u"¿©"
JOB_SPRITES_PATH_PREFIX = u"sprite/ÀÎ°£Á·/¸öÅë"

JOB_TO_SPR_MAP = {
    0: (u"ÃÊº¸ÀÚ_³².spr", "Novice"),
    4046: (u"ÅÂ±Ç¼Ò³â_³².spr", "Taekwon")
}


def get_char_body_path(char, rodata_path):
    # return os.path.join(rodata_path,
    #                     JOB_SPRITES_PATH_PREFIX,
    #                     MALE if char.sex == "M" else FEMALE,
    #                     JOB_TO_SPR_MAP.get(getattr(char, "class")))

    cl = getattr(char, "class")
    if cl in JOB_TO_SPR_MAP:
        return u"/".join([rodata_path,
                         JOB_SPRITES_PATH_PREFIX,
                         MALE if char.sex == "M" else FEMALE,
                         JOB_TO_SPR_MAP[cl][0]])
    else:
        return None
