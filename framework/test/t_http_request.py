#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import os
from os import path
import StringIO
import sys
#import webtest
#from wsgiref import handlers
from wsgiref import validate
import unittest

from framework import application
from framework import http_request
from framework.test import server_config

#from userapp import config
#from userapp import post_controller


class TestCHttpRequestWebTest(unittest.TestCase):
    """Http Requestのテストを行う。
    """

    def setUp(self):
        self.application = validate.validator(server_config.server_normal)

    # 環境依存なので同テストをUnitテストに移行.
    #def test_redirect(self):
        #"""リダイレクトのテストを行う。
        #"""

        #app = webtest.TestApp(self.application)
        #response = app.post('/', params='a=post&p=9&name=WebTest&title=This is redirect test&content=ignore this')
        #self.assertEqual('301 Moved Permanently', response.status)

        ## redirectをfollow()
        #redirect_response = response.follow()
        #self.assertEqual('200 OK', redirect_response.status)


class TestCHttpRequestUnit(unittest.TestCase):

    def setUp(self):
        # アプリケーションデータの準備.
        parent_rel = os.sep + '..' + os.sep + '..' + os.sep
        env = {
                'REQUEST_METHOD': 'GET',
                'DOCUMENT_ROOT': path.abspath(path.dirname(__file__) + parent_rel)}
        io = StringIO.StringIO()

        # インスタンスの生成.
        self.app = application.CApplication(env, None, io)
        self.request = http_request.CHttpRequest(self.app, None)

    def test_init(self):
        """初期化処理をテストする。
        """

        self.assertIsInstance(self.app, application.CApplication)
        self.assertIsInstance(self.request, http_request.CHttpRequest)
        self.assertEqual(self.app, self.request.app)

    def test_init_response(self):
        """start_responseの初期化設定をテストする。
        """

        def start_response(status, response):
            pass

        self.request = http_request.CHttpRequest(self.app, start_response)
        self.assertEqual(start_response, self.request.start_response)

    def test_get(self):
        """GET要求をテストする。
        """

        self.request.init_request()
        self.assertTrue(self.request.is_get())
        self.assertFalse(self.request.is_post())
        self.assertFalse(self.request.params)

    def test_post(self):
        """POST要求をテストする。
        """

        self.app.env['REQUEST_METHOD'] = "POST"
        io = StringIO.StringIO()
        self.app.env['wsgi.input'] = io
        io.write("c=post&a=view")
        io.seek(0)

        self.request.init_request()
        self.assertTrue(self.request.is_post())
        self.assertFalse(self.request.is_get())
        self.assertIn('a', self.request.params)
        self.assertEqual('view', self.request.param('a'))
        self.assertNotIn('b', self.request.params)
        self.assertIn('c', self.request.params)
        self.assertEqual('post', self.request.param('c'))

        io.close()

    def test_incorrect_method(self):
        """不正なREQUEST_METHODをテストする。
        """

        self.app.env['REQUEST_METHOD'] = "PUT"
        with self.assertRaises(SystemExit):
            self.request.init_request()

    def test_no_method(self):
        """空のREQUEST_METHODをテストする。
        """

        self.app.env['REQUEST_METHOD'] = ""
        with self.assertRaises(SystemExit):
            self.request.init_request()

    def test_response_no_status(self):
        """status codeが存在しない場合のレスポンス出力をテストする。
        """

        self.request.status_code = 0
        self.assertEqual(0, self.request.output_response_header())

    def test_response_start(self):
        """start_responseが設定されている場合のレスポンス出力をテストする。
        """

        # printされた文字列を判定するために標準出力をバッファに切り替え.
        io = StringIO.StringIO()
        sys.stdout = io

        def start_response(status, response):
            print 'exec start_response({0})'.format(status)

        self.request.start_response = start_response
        self.request.output_response_header()

        self.assertIn('exec start_response(200 OK)', io.getvalue())

    def test_response_not_start(self):
        """start_responseが設定されていない場合のレスポンス出力をテストする。
        """

        # printされた文字列を判定するために標準出力をバッファに切り替え.
        io = StringIO.StringIO()
        sys.stdout = io

        self.request.start_response = None
        self.request.output_response_header()

        self.assertIn('Content-type: text/html; charset=utf-8', io.getvalue())

    def test_response_headers(self):
        """追加したヘッダのレスポンス出力をテストする。
        """

        # printされた文字列を判定するために標準出力をバッファに切り替え.
        io = StringIO.StringIO()
        sys.stdout = io

        def start_response(status, response):
            for h, v in response:
                print '{0}: {1}'.format(h, v)

        self.request.start_response = start_response
        self.request.headers['Location'] = 'http://example.com/'
        self.request.headers['webtest'] = 'test'
        self.request.output_response_header()

        self.assertIn('Content-type: text/html; charset=utf-8', io.getvalue())
        self.assertIn('Location: http://example.com/', io.getvalue())
        self.assertIn('webtest: test', io.getvalue())

    def test_response_code(self):
        """レスポンスコードの変換をテストする。
        """

        # int型.
        self.assertEqual('OK', self.request.get_response_code(200))
        self.assertEqual('HTTP Version Not Supported', self.request.get_response_code(505))

        # 文字列型.
        self.assertEqual('OK', self.request.get_response_code('200'))
        self.assertEqual('HTTP Version Not Supported', self.request.get_response_code('505'))

        # 変換テーブルにない.
        self.assertEqual(None, self.request.get_response_code(199))
        self.assertEqual(None, self.request.get_response_code(506))

        # intでもstrでもない.
        self.assertEqual(None, self.request.get_response_code(['200']))

    def test_redirect(self):
        """リダイレクトのテストを行う。
        """

        # 設定されていない辞書キーへのアクセスは例外が発生.
        with self.assertRaises(KeyError):
            self.request.headers['Location']

        self.request.redirect('http://example.com/')
        self.assertEqual(self.request.status_code, 0)  # output_response_header()で0に変更される仕様.
        self.assertTrue(self.request.headers['Location'])

if __name__ == '__main__':
    unittest.main()
