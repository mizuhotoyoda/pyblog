#!/usr/bin/python2.7
# vim: fileencoding=utf-8

#import codecs
import os
#import sys
import unittest


if __name__ == '__main__':
    #sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    #print 'Content-Type: text/html; charset=utf-8'
    #print

    # 実行するテストを追加.
    this_dir = os.path.dirname(__file__)
    this_dir += './userapp/test'
    suite = unittest.TestLoader().discover(start_dir=this_dir, pattern='t_*.py')

    # テスト実行.
    unittest.TextTestRunner(verbosity=2).run(suite)
