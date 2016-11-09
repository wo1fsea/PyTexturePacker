# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/11/06
Description:
    test.py
----------------------------------------------------------------------------"""

import unittest

TEST_MODULE = "tests"
TEST_CASE_NAME = "^test[\w]+\.py$"


def load_test_suite():
    import unittest
    import re
    import os

    test_path = os.path.abspath(TEST_MODULE)
    files = os.listdir(test_path)

    test_file_re = re.compile(TEST_CASE_NAME, re.IGNORECASE)
    files = filter(test_file_re.match, files)

    module_names = map(lambda f: os.path.splitext(f)[0], files)
    modules = map(lambda x: __import__("%s.%s" % (TEST_MODULE, x), fromlist=[TEST_MODULE]), module_names)

    return unittest.TestSuite(map(unittest.defaultTestLoader.loadTestsFromModule, modules))


if __name__ == '__main__':
    a = load_test_suite()
    unittest.main(defaultTest="load_test_suite")
