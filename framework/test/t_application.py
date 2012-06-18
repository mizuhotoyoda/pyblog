#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import os
from os import path
import StringIO
import webtest
#from wsgiref import handlers
from wsgiref import validate
import unittest

from framework import application
from framework import http_request
from framework.test import server_config

from userapp import config
from userapp import post_controller


class TestCApplicationRun(unittest.TestCase):
    """webtestを利用して、ページの表示についてテストする。
    """

    def setUp(self):
        self.application = validate.validator(server_config.server_normal)

    def test_root(self):
        """Topページの表示をテストする。
        """

        app = webtest.TestApp(self.application)
        response = app.get('/')
        self.assertEqual('200 OK', response.status)

    def test_view_action(self):
        """viewアクションをテストする。
        """

        app = webtest.TestApp(self.application)
        response = app.get('/', params={
            "a": "view",
            })
        self.assertEqual('200 OK', response.status)

    def test_no_method(self):
        """不正なREQUEST_METHODをテストする。
        """

        # REQUEST_METHODに空文字を設定.
        app = webtest.TestApp(self.application, extra_environ={"REQUEST_METHOD": ""})
        with self.assertRaises(SystemExit):
            app.get('/')

    def test_post_method(self):
        """POST要求をテストする。
        """

        app = webtest.TestApp(self.application)
        response = app.post('/')
        self.assertEqual('200 OK', response.status)


class TestCApplicationUnit(unittest.TestCase):

    def setUp(self):
        # アプリケーションデータの準備.
        parent_rel = os.sep + '..' + os.sep + '..' + os.sep
        env = {
                'REQUEST_METHOD': 'GET',
                'DOCUMENT_ROOT': path.abspath(path.dirname(__file__) + parent_rel)}
        io = StringIO.StringIO()

        # インスタンスの生成.
        self.app = application.CApplication(env, None, io)
        self.app_config = config.MainConfig(self.app)
        self.controller = post_controller.CPostController(self.app)

    def test_init(self):
        self.assertIsInstance(self.app, application.CApplication)
        self.assertIsInstance(self.app.request, http_request.CHttpRequest)

    def test_run(self):
        self.app.run(self.app_config, self.controller)

if __name__ == '__main__':
    unittest.main()
