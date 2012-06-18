#!/usr/bin/python2.7
# vim: fileencoding=utf-8

import os
#パッケージの索引は付けない。(パフォーマンスが問題になってから)


def load_tests(loader, standard_tests, pattern):
    # top level directory cached on loader instance
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern='t_*.py')
    standard_tests.addTests(package_tests)
    return standard_tests
