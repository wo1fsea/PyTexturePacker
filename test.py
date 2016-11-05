import unittest

TEST_MODULE = "Test"
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

    importer = lambda x: __import__("%s.%s" % (TEST_MODULE, x), fromlist=[TEST_MODULE])
    modules = map(importer, module_names)

    return unittest.TestSuite(map(unittest.defaultTestLoader.loadTestsFromModule, modules))


if __name__ == '__main__':
    a = load_test_suite()
    unittest.main(defaultTest="load_test_suite")
