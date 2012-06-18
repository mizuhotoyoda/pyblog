#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import copy
import re
from xml.sax import saxutils

from framework import base
from framework import controller_base
from userapp import post_model
from userapp import datetimelib


class CPostController(controller_base.CControllerBase):
    def __init__(self, app):
        controller_base.CControllerBase.__init__(self, app)

    def action_index(self):
        model = post_model.CPostModel(self.app)
        data = {'id': '', 'name': '', 'stat': '', 'date': '', 'title': '', 'content': '', 'navi': ''}

        id = self.app.request.param('id')
        if id:
            doc = model.get_document(id)
        else:
            doc = model.get_latest()

        if doc:
            data['id'] = str(doc['_id'])
            data['name'] = saxutils.escape(doc['name'].encode('utf-8'))
            data['stat'] = str(doc['stat'])
            dt = datetimelib.CDateTime
            data['date'] = dt.convert_iso_string(doc['sub_date'].encode('utf-8'))
            data['title'] = saxutils.escape(doc['title'].encode('utf-8'))
            data['content'] = re.sub(r'\n', '<br />', doc['content'].encode('utf-8'))

            # ナビゲーションの生成.
            data['navi'] = NaviCreator.create_navi(self.app, doc)

        self.render_view('index.html', data)

    def action_post(self):
        req = self.app.request

        if not req.is_post():  # POST以外は拒否.
            raise Exception('your request is denied')

        model = post_model.CPostModel(self.app)
        model.name = req.param('name')
        model.title = req.param('title')
        model.content = req.param('content')
        model.delkey = req.param('delkey')

        # 入力必須項目のチェック.
        if not model.check_post():
            raise Exception('入力必要項目について入力して下さい。')

        proc = req.param('p')

        if proc is "9":  # procが9の場合、テストモードとして、実際の書き込みを行わない.
            req.redirect('/')
        elif proc is "3":  # procが3の場合に書きこみ処理を行う.
            model.write_post()
            req.redirect('/?id={0}'.format(model.id))
        else:
            raise Exception('不正な要求です。')

    def action_delete(self):
        req = self.app.request

        if not req.is_post():  # POST以外は拒否.
            raise Exception('your request is denied')

        model = post_model.CPostModel(self.app)
        model.id = req.param('id')
        model.delkey = req.param('delkey')

        proc = req.param('p')

        if proc is "9":  # procが9の場合、テストモードとして、実際の削除を行わない.
            req.redirect('/')
        elif proc is "3":  # procが3の場合に書きこみ処理を行う.
            model.delete_post()
            req.redirect('/')
        else:
            raise Exception('不正な要求です。')


class NaviCreator(base.CBase):
    @staticmethod
    def create_navi(app, cur_doc):
        if not cur_doc:
            return '&nbsp;'

        model = post_model.CPostModel(app)
        col = model.get_collection()

        if col.count() <= 1:  # 投稿が1件存在する場合.
            return '&nbsp;'

        # 現在の投稿、その前の投稿、その次の投稿、最新の投稿をそれぞれ探す.
        previous = None
        current = None
        after = None
        last = None
        is_found = False
        for doc in col:
            if not is_found and cur_doc['_id'] == doc['_id']:  # 現在の投稿が見つかった.
                current = copy.copy(doc['_id'])
                previous = copy.copy(last)
                is_found = True
            elif is_found and current == last:  # 現在の投稿の次の投稿である.
                after = copy.copy(doc['_id'])
            last = copy.copy(doc['_id'])

        navi = NaviCreator.convert_colid_to_navi(current, previous, after, last)
        return navi

    @staticmethod
    def convert_colid_to_navi(current, previous, after, last):
        if not current:  # 現在表示中の投稿があるにも関わらず、find()で見つからないのは想定外.
            raise Exception('unexpected behavior in creating navigation')

        if last and last != current:  # 最新の投稿リンクを作成.
            last = '<a href="/?id={0}">最新の投稿へ</a>'.format(str(last))
        else:
            last = '最新の投稿へ'

        if previous and previous != current:  # 最新の投稿リンクを作成.
            old = '<a href="/?id={0}">古い投稿へ</a>'.format(str(previous))
        else:
            old = '古い投稿へ'

        if after and after != current:  # 最新の投稿リンクを作成.
            new = '<a href="/?id={0}">新しい投稿へ</a>'.format(str(after))
        else:
            new = '新しい投稿へ'

        return NaviCreator.complement_navi(last, new, old)

    @staticmethod
    def complement_navi(last, new, old):
        navi = last
        if new:
            if navi:
                navi += ' | '
            navi += new
        if old:
            if navi:
                navi += ' | '
            navi += old

        return navi
