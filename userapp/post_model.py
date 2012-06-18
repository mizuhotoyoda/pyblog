#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import bson
import pymongo

from framework import model_base
from userapp import datetimelib


class CPostModel(model_base.CModelBase):
    def __init__(self, app):
        model_base.CModelBase.__init__(self, app, 'pyblog', 'post')
        self.stat = ''
        self.sub_date = ''
        self.name = ''
        self.title = ''
        self.content = ''

    def get_collection(self, is_desc=False):
        sort_order = pymongo.DESCENDING if is_desc else pymongo.ASCENDING
        return self.col.find().sort('sub_date', sort_order)

    def get_document(self, id):
        return self.col.find_one(bson.objectid.ObjectId(id))

    def get_latest(self):
        if not self.col.find().count():
            return None

        return self.get_collection()[0]

    def check_post(self):
        """投稿内容の確認。
        """

        if not self.name or not self.title or not self.content:
            return False

        return True

    def write_post(self):
        """新規投稿を行う。
        """

        #self.name = unicode(self.name)
        #self.title = unicode(self.title)
        #self.content = unicode(self.content)

        if not self.check_post():
            raise Exception('投稿内容が不正です。')

        id = self.col.insert({'stat': 0, 'delkey': self.delkey, 'sub_date': datetimelib.CDateTime.get_now(), 'name': self.name, 'title': self.title, 'content': self.content}, sefe=True)
        self.id = id

    def delete_post(self):
        """投稿を削除する。
        """

        # 設定値の確認.
        if not self.id:
            raise Exception('不正な要求です。')

        doc = self.get_document(self.id)
        if not doc:
            raise Exception('指定された投稿が存在しません。')

        if not doc['delkey'] or self.delkey != doc['delkey']:
            raise Exception('削除キーが異なります。')

        self.col.remove(bson.objectid.ObjectId(self.id))
