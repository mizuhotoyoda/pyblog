#!/usr/bin/python2.7
# vim: fileencoding=utf-8

from framework import base


class ConfigBase(base.CBase):
    """ConfigBase is the base class for the application config class.
    """

    def __init__(self, app):
        base.CBase.__init__(self)
        self.app = app
