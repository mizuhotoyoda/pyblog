#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import errno
import os
from os import path
import string

from framework import base


class CControllerBase(base.CBase):
    """CControllerBase is the base class for all controller classes.
    """

    def __init__(self, app):
        base.CBase.__init__(self)
        self.app = app

    def start_action(self, action):
        if not isinstance(action, str):
            raise Exception('指定されたアクションが不正です。')

        getattr(self, 'action_' + action)()

    def render_view(self, view_file, params=None):
        """指定されたviewの描画を行う。
        """

        if params is None:
            params = {}

        dir_path = self.app.request.base_url
        dir_path = dir_path + 'userapp' + os.sep + 'view' + os.sep
        view_file = dir_path + view_file  # view_fileの絶対パスを生成.

        if not path.exists(view_file):  # viewファイルが存在しない場合.
            errmsg = "the view file is not found that you specified it:{0}"
            raise IOError((errno.ENOENT, errmsg.format(view_file)))

        # viewファイルを読み取り.
        file = open(view_file, 'r')
        view_buffer = file.read()
        file.close()

        # テンプレート処理.
        if len(params):
            template = string.Template(view_buffer)
            view_buffer = template.substitute(params)

        layout_file = dir_path + 'layout.html'  # layout_fileの絶対パスを生成.
        if not path.exists(layout_file):  # layoutファイルが存在しない場合.
            errmsg = "the layout view file is not found:{0}"
            raise IOError((errno.ENOENT, errmsg.format(view_file)))

        # layoutファイルを読み取り.
        file = open(layout_file, 'r')
        layout_buffer = file.read()
        file.close()

        # layoutファイルにテンプレートを埋め込む.
        template = string.Template(layout_buffer)
        full_buffer = template.substitute(main=view_buffer)

        print full_buffer
