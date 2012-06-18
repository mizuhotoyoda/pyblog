#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import os
from os import path
import re
import StringIO
import sys
import webtest
#from wsgiref import handlers
from wsgiref import validate
import unittest

from framework import application
from userapp import post_controller
from framework.test import server_config

#from userapp import config
#from userapp import post_controller


class TestCPostControllerRun(unittest.TestCase):
    """webtestを利用して、PostControllerをテストする。
    """

    def setUp(self):
        io = StringIO.StringIO()
        sys.stdout = io

        self.application = validate.validator(server_config.server_normal)

        # 準備データの投稿.
        app = webtest.TestApp(self.application)
        self.condition = [
                {'id': '', 'title': 'ready_post1', 'content': 'ready_post1'},
                {'id': '', 'title': 'ready_post2', 'content': 'ready_post2'}]

        for dic in self.condition:
            response = app.post('/', params='a=post&p=3&delkey=0000&name=WebTest&title={0}&content={1}'.format(dic['title'], dic['content']))
            self.assertEqual('301 Moved Permanently', response.status)
            redirect_response = response.follow()
            self.assertEqual('200 OK', redirect_response.status)
            pattern = r'<a href="/\?id=([0-9a-zA-Z]+)">{0}</a>'.format(dic['title'])
            dic['id'] = re.search(pattern, redirect_response.body).group(1)
            self.assertTrue(len(dic['id']) == 24)

    def tearDown(self):
        app = webtest.TestApp(self.application)
        for dic in self.condition:
            response = app.post('/', params='a=delete&p=3&delkey=0000&id={0}'.format(dic['id']))
            self.assertEqual('301 Moved Permanently', response.status)
            redirect_response = response.follow()
            self.assertEqual('200 OK', redirect_response.status)

    def test_id_none(self):
        """投稿IDの指定なしでTopページの表示をテストする。
        """

        io = StringIO.StringIO()
        sys.stdout = io

        app = webtest.TestApp(self.application)
        response = app.get('/')
        self.assertEqual('200 OK', response.status)

    def test_id_specified(self):
        """投稿IDを指定して、Topページの表示をテストする。
        """

        io = StringIO.StringIO()
        sys.stdout = io

        app = webtest.TestApp(self.application)
        response = app.get('/', params='id={0}'.format(self.condition[0]['id']))
        self.assertEqual('200 OK', response.status)

    def test_post(self):
        """投稿をテストする。
        """

        app = webtest.TestApp(self.application)
        response = app.post('/', params='a=post&p=9&name=WebTest&title=This is post test&content=ignore this')
        self.assertEqual('301 Moved Permanently', response.status)

        # redirectをfollow()
        redirect_response = response.follow()
        self.assertEqual('200 OK', redirect_response.status)


class TestCPostControllerUnit(unittest.TestCase):

    def setUp(self):
        # アプリケーションデータの準備.
        parent_rel = os.sep + '..' + os.sep + '..' + os.sep
        env = {
                'REQUEST_METHOD': 'GET',
                'DOCUMENT_ROOT': path.abspath(path.dirname(__file__) + parent_rel)}
        io = StringIO.StringIO()

        # インスタンスの生成.
        self.app = application.CApplication(env, None, io)
        self.post_controller = post_controller.CPostController(self.app)
        self.app.request.init_request()

    def test_init(self):
        """初期化処理をテストする。
        """

        # インスタンス生成チェック.
        self.assertIsInstance(self.app, application.CApplication)
        self.assertIsInstance(self.post_controller, post_controller.CPostController)

        # メンバー変数整合チェック.
        self.assertEqual(self.app, self.post_controller.app)

if __name__ == '__main__':
    unittest.main()
