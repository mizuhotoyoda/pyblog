#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import sys

from framework import base
from framework import http_request


class CApplication(base.CBase):
    """CApplication decides a path of a user request to the controller as MVC pattern.
    """

    def __init__(self, environ, start_response, io):
        base.CBase.__init__(self)
        self.env = environ
        self.io = io

        self.request = http_request.CHttpRequest(self, start_response)

    def run(self, config, controller):
        self.config = config
        self.controller = controller

        # 標準出力をStringIOに設定.
        sys.stdout = self.io

        # CHttpRequestを生成し、リクエストを処理します.
        self.request.init_request()

        # Get Controller(デフォルトコントローラしか実装出来ないというへたれ仕様ということで…)
        #self.defaultController = request.param("c")

        # Get Action
        self.action = self.request.param("a")

        # actionが設定されていない場合、"index"を初期値とする.
        if not self.action:
            self.action = "index"

        # actionの開始.
        try:
            self.controller.start_action(self.action)
        except Exception as exp:
            print 'exception is occured', exp

        # 標準出力を元に戻すに.
        sys.stdout = sys.__stdout__

        # 最後にレスポンスを出力.
        self.request.output_response_header()

    def exit(self):
        sys.exit()
