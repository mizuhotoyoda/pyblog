#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import cgitb
import codecs
import os
from os import path
import sys
import StringIO

from framework import application

from userapp import config
from userapp import post_controller


def server_normal(environ, start_response):
    """ WSGIアプリケーションを開始します。

    WSGIアプリケーションではprintが使えないので、StringIOに出力する文字列を書きこんでいく.
    """
    #for debug.
    cgitb.enable()

    #IOを設定.
    io = StringIO.StringIO()

    #標準出力でunicodeを取り扱う.
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    #output content type
    #start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])

    #環境の初期化.
    environ['DOCUMENT_ROOT'] = path.abspath(path.dirname(__file__) + os.sep + '..' + os.sep + '..' + os.sep)
    app = application.CApplication(environ, start_response, io)
    app_config = config.MainConfig(app)
    controller = post_controller.CPostController(app)

    #WEBアプリケーションを開始する.
    app.run(app_config, controller)

    print environ['DOCUMENT_ROOT']

    #IOの先頭にシーク.(これをしないとIOに書き込んだ文字列が出力されない.)
    io.seek(0)

    return io
