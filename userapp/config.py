#!/usr/bin/python2.7
# vim: fileencoding=utf-8

#import sys
#import os
#import cgi

#import framework.model.CModelBase
from framework import config_base


class MainConfig(config_base.ConfigBase):
    def __init__(self, app):
        config_base.ConfigBase.__init__(self, app)
