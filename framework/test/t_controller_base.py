#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import os
from os import path
import StringIO
import unittest

from framework import application
from framework import controller_base

#from userapp import config
#from userapp import post_controller


class TestCControllerBaseUnit(unittest.TestCase):

    def setUp(self):
        # アプリケーションデータの準備.
        parent_rel = os.sep + '..' + os.sep + '..' + os.sep
        env = {
                'REQUEST_METHOD': 'GET',
                'DOCUMENT_ROOT': path.abspath(path.dirname(__file__) + parent_rel)}
        io = StringIO.StringIO()

        # インスタンスの生成.
        self.app = application.CApplication(env, None, io)
        self.controller_base = controller_base.CControllerBase(self.app)

    def test_init(self):
        """初期化処理をテストする。
        """

        self.assertIsInstance(self.app, application.CApplication)
        self.assertIsInstance(self.controller_base, controller_base.CControllerBase)
        self.assertEqual(self.app, self.controller_base.app)

    def test_action(self):
        """start_action()をテストする。
        """

        class ActionTestController(controller_base.CControllerBase):
            def __init__(self, app):
                controller_base.CControllerBase.__init__(self, app)

            def action_test(self):
                return None

        self.test_controller = ActionTestController(self.app)

        self.test_controller.start_action('test')
        with self.assertRaises(Exception):
            self.test_controller.start_action(0)
        with self.assertRaises(AttributeError):
            self.test_controller.start_action('index')

    def test_render(self):
        """render_view()をテストする。

        正常系はviewファイルの名前に依存するため、ユーザアプリ側のテストで行う。
        """

        class RenderTestController(controller_base.CControllerBase):
            def __init__(self, app, state):
                controller_base.CControllerBase.__init__(self, app)
                self.state = state

            def action_test(self):
                if self.state is 1:  # viewファイルが存在しない場合.
                    self.render_view('???')
                else:
                    raise Exception("test error:be set unkown state")

        self.test_controller = RenderTestController(self.app, 1)
        with self.assertRaises(IOError):
            self.test_controller.start_action('test')

    def none(self):
        pass

if __name__ == '__main__':
    unittest.main()
