import os
import yaml

import logging
import logging.config


def create():
    log = logging.getLogger("ragnaweb")

    if len(log.handlers) == 0:
        fdir = os.path.dirname(os.path.abspath(__file__))
        log_cfg_file = os.path.join(fdir, "logging.conf")
        with open(log_cfg_file, "r") as f:
            log_cfg_data = yaml.load(f, Loader=yaml.FullLoader)
        logging.config.dictConfig(log_cfg_data)

    return log
