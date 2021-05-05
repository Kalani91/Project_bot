# -*- coding: utf-8 -*-
#
# Author: Chuan He
# Created on 04/05/2021
# Last edit: 05/05/2021

import logging.config
import yaml

def setup_logging(default_path='utils/logger_conf.yaml', default_level=logging.INFO):
    path = default_path
    try:
        with open(default_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
    except:
        logging.basicConfig(level=default_level)
