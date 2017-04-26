# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/11/29
Description:
    TestMaxRectsAtlas.py
----------------------------------------------------------------------------"""

import unittest
from PyTexturePacker.MaxRectsPacker import MaxRectsAtlas
from PyTexturePacker import Rect


class TestMaxRectsAtlas(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _test_expand1(self):
        def gen_and_expand(width, height, method):
            tmp = MaxRectsAtlas.MaxRectsAtlas(w, h)
            tmp.expand(method)
            return tmp

        w = h = 2
        m = MaxRectsAtlas.MaxRectsAtlas.EXPAND_WIDTH
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w * 2, h))

        w = h = 2
        m = MaxRectsAtlas.MaxRectsAtlas.EXPAND_HEIGHT
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w, h * 2))

        w = 2
        h = 1
        m = MaxRectsAtlas.MaxRectsAtlas.EXPAND_SHORT_SIDE
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w, h * 2))

        w = 2
        h = 1
        m = MaxRectsAtlas.MaxRectsAtlas.EXPAND_LONG_SIDE
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w * 2, h))

        w = h = 2
        m = MaxRectsAtlas.MaxRectsAtlas.EXPAND_BOTH
        test_object = gen_and_expand(w, h, m)
        self.assertSequenceEqual(test_object.size, (w * 2, h * 2))

    def _test_expand2(self):
        w = h = 2
        m = MaxRectsAtlas.MaxRectsAtlas.EXPAND_BOTH
        test_object = MaxRectsAtlas.MaxRectsAtlas(w, h)
        test_object.max_rect_list = []
        test_object.max_rect_list.append(Rect.Rect(0, 0, 2, 2))
        test_object.expand(m)
        self.assertEqual(len(test_object.max_rect_list), 1)
        self.assertEqual(test_object.max_rect_list[0].width, 4)
        self.assertEqual(test_object.max_rect_list[0].height, 4)

        w = h = 2
        m = MaxRectsAtlas.MaxRectsAtlas.EXPAND_BOTH
        test_object = MaxRectsAtlas.MaxRectsAtlas(w, h)
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
        w = h = 2
        self.test_object = MaxRectsAtlas.MaxRectsAtlas(w, h)
        main = Rect.Rect(1, 1, 3, 3)

        sub0 = Rect.Rect(0, 1, 1, 1)
        sub1 = Rect.Rect(1, 0, 1, 1)
        sub2 = Rect.Rect(0, 3, 1, 1)
        sub3 = Rect.Rect(3, 0, 1, 1)

        self.assertSequenceEqual(self.test_object.cut(main, sub0), [main])
        self.assertSequenceEqual(self.test_object.cut(main, sub1), [main])
        self.assertSequenceEqual(self.test_object.cut(main, sub2), [main])
        self.assertSequenceEqual(self.test_object.cut(main, sub3), [main])

        self.assertSequenceEqual(self.test_object.cut(main, main), [])

        sub4 = Rect.Rect(2, 2, 1, 1)

        self.assertSequenceEqual(self.test_object.cut(main, sub4), [Rect.Rect(1, 1, 1, 3),
                                                                    Rect.Rect(1, 1, 3, 1),
                                                                    Rect.Rect(3, 1, 1, 3),
                                                                    Rect.Rect(1, 3, 3, 1)])

    def test_rank(self):
        w = h = 2
        main = Rect.Rect(0, 0, 1, 2)
        self.test_object = MaxRectsAtlas.MaxRectsAtlas(w, h)

        r0 = self.test_object.rank(main, Rect.Rect(0, 0, 0.9, 1), self.test_object.RANK_BSSF)
        r1 = self.test_object.rank(main, Rect.Rect(0, 0, 0.1, 1.9), self.test_object.RANK_BSSF)
        self.assertLess(r0, r1)

        r0 = self.test_object.rank(main, Rect.Rect(0, 0, 0.1, 1.9), self.test_object.RANK_BLSF)
        r1 = self.test_object.rank(main, Rect.Rect(0, 0, 0.9, 1), self.test_object.RANK_BLSF)
        self.assertLess(r0, r1)

        r0 = self.test_object.rank(main, Rect.Rect(0, 0, 0.5, 1.5), self.test_object.RANK_BAF)
        r1 = self.test_object.rank(main, Rect.Rect(0, 0, 0.1, 1.9), self.test_object.RANK_BAF)
        self.assertLess(r0, r1)
