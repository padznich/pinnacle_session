
# -*- coding: utf-8 -*-

import os

import ConfigParser


ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")

config = ConfigParser.ConfigParser()
config.readfp(open(os.path.join(ROOT, "conf/conf.ini")))

creds_dict = dict(config.items("creds"))


class Conf(object):

    def __init__(self, d):
        self.__dict__.update(d)


creds = Conf(creds_dict)
