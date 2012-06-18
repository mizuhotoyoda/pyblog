#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import cgitb
#import codecs
import StringIO
#import sys
import wsgiref.handlers

from framework import application

from userapp import config
from userapp import post_controller


def start_application(environ, start_response):
    """ WSGIアプリケーションを開始します。

    WSGIアプリケーションではprintが使えないので、StringIOに出力する文字列を書きこんでいく.
    """
    #for debug.
    cgitb.enable()

    #IOを設定.
    io = StringIO.StringIO()

    #標準出力でunicodeを取り扱う.
    #sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    #環境の初期化.
    app = application.CApplication(environ, start_response, io)
    app_config = config.MainConfig(app)
    controller = post_controller.CPostController(app)

    #WEBアプリケーションを開始する.
    app.run(app_config, controller)

    #for debug
    #io.write("<br />スクリプトEND")

    return io.getvalue()

if __name__ == "__main__":
    #CGI用のWSGIアプリケーションを開始.
    wsgiref.handlers.CGIHandler().run(start_application)
