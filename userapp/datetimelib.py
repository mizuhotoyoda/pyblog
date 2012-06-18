#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import datetime
import isodate

from framework import base


class CDateTime(base.CBase):
    def __init__(self):
        base.CBase.__init__(self)

    @staticmethod
    def convert_iso_string(iso):
        dt = isodate.parse_datetime(iso)
        return dt.strftime('%Y年%m月%d日 %H時%M分')

    @staticmethod
    def get_now():
        return datetime.datetime.now().isoformat()
