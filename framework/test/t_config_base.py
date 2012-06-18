#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import os
from os import path
import StringIO
import unittest

from framework import application
from framework import config_base

#from userapp import config
#from userapp import post_controller


class TestConfigBaseUnit(unittest.TestCase):

    def setUp(self):
        # アプリケーションデータの準備.
        parent_rel = os.sep + '..' + os.sep + '..' + os.sep
        env = {
                'REQUEST_METHOD': 'GET',
                'DOCUMENT_ROOT': path.abspath(path.dirname(__file__) + parent_rel)}
        io = StringIO.StringIO()

        # インスタンスの生成.
        self.app = application.CApplication(env, None, io)
        self.config_base = config_base.ConfigBase(self.app)

    def test_init(self):
        """初期化処理をテストする。
        """

        self.assertIsInstance(self.app, application.CApplication)
        self.assertIsInstance(self.config_base, config_base.ConfigBase)
        self.assertEqual(self.app, self.config_base.app)

if __name__ == '__main__':
    unittest.main()
