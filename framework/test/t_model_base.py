#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import os
from os import path
import StringIO
import unittest

from framework import application
from framework import model_base

#from userapp import config
#from userapp import post_controller


class TestCModelBaseUnit(unittest.TestCase):

    def setUp(self):
        # アプリケーションデータの準備.
        parent_rel = os.sep + '..' + os.sep + '..' + os.sep
        env = {
                'REQUEST_METHOD': 'GET',
                'DOCUMENT_ROOT': path.abspath(path.dirname(__file__) + parent_rel)}
        io = StringIO.StringIO()

        # インスタンスの生成.
        self.app = application.CApplication(env, None, io)
        self.model_base = model_base.CModelBase(self.app, 'pyblog', 'post')

    def test_init(self):
        """初期化処理をテストする。
        """

        self.assertIsInstance(self.app, application.CApplication)
        self.assertIsInstance(self.model_base, model_base.CModelBase)
        self.assertEqual(self.app, self.model_base.app)

if __name__ == '__main__':
    unittest.main()
