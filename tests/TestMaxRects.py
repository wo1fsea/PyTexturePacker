# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/11/29
Description:
    TestMaxRects.py
----------------------------------------------------------------------------"""

import unittest
from PyTexturePacker.MaxRectsBinPacker import MaxRects
from PyTexturePacker import Rect


class TestMaxRects(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_expand1(self):
        def gen_and_expand(width, height, method):
            tmp = MaxRects.MaxRects(w, h)
            tmp.expand(method)
            return tmp

        w = h = 2
        m = MaxRects.MaxRects.EXPAND_WIDTH
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w * 2, h))

        w = h = 2
        m = MaxRects.MaxRects.EXPAND_HEIGHT
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w, h * 2))

        w = 2
        h = 1
        m = MaxRects.MaxRects.EXPAND_SHORT_SIDE
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w, h * 2))

        w = 2
        h = 1
        m = MaxRects.MaxRects.EXPAND_LONG_SIDE
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w * 2, h))

        w = h = 2
        m = MaxRects.MaxRects.EXPAND_BOTH
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w * 2, h * 2))

    def _test_expand2(self):
        w = h = 2
        m = MaxRects.MaxRects.EXPAND_BOTH
        test_object = MaxRects.MaxRects(w, h)
        test_object.max_rect_list = []
        test_object.max_rect_list.append(Rect.Rect(0, 0, 2, 2))
        test_object.expand(m)
        self.assertEqual(len(test_object.max_rect_list), 1)
        self.assertEqual(test_object.max_rect_list[0].width, 4)
        self.assertEqual(test_object.max_rect_list[0].height, 4)

        w = h = 2
        m = MaxRects.MaxRects.EXPAND_BOTH
        test_object = MaxRects.MaxRects(w, h)
        test_object.max_rect_list = []
        test_object.max_rect_list.append(Rect.Rect(0, 0, 1, 1))
        test_object.expand(m)
        self.assertEqual(len(test_object.max_rect_list), 3)

        size_list = [(1, 1), (2, 4), (4, 2)]
        r = test_object.max_rect_list[0]
        self.assertIn((r.width, r.height), size_list)
        r = test_object.max_rect_list[1]
        self.assertIn((r.width, r.height), size_list)
        r = test_object.max_rect_list[2]
        self.assertIn((r.width, r.height), size_list)

    def test_expand(self):
        self._test_expand1()
        self._test_expand2()

    def test_cut(self):
        pass

    def test_rank(self):
        pass
