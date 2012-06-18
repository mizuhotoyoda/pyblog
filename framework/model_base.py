#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import pymongo

from framework import base


class CModelBase(base.CBase):
    """CModelBase is the base class for classes accessing a database.
    """

    def __init__(self, app, db, collection):
        base.CBase.__init__(self)
        self.app = app
        connection = pymongo.Connection('127.0.0.1', 27017)
        self.db = connection[db]
        self.col = self.db[collection]
