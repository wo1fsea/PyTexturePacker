# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/11/10
Description:
    TestRect.py
----------------------------------------------------------------------------"""

import unittest
import random
from PyTexturePacker import Rect


class TestRect(unittest.TestCase):
    def setUp(self):
        self.x = random.randint(0, 1024)
        self.y = random.randint(0, 1024)
        self.w = random.randint(1, 1024)
        self.h = random.randint(1, 1024)

        self.test_object = Rect.Rect(self.x, self.y, self.w, self.h)

    def tearDown(self):
        pass

    def check_property(self):
        self.assertEqual(self.test_object.x, self.x)
        self.assertEqual(self.test_object.y, self.y)
        self.assertEqual(self.test_object.width, self.w)
        self.assertEqual(self.test_object.height, self.h)

        self.assertEqual(self.test_object.left, self.x)
        self.assertEqual(self.test_object.right, self.x + self.w)
        self.assertEqual(self.test_object.top, self.y)
        self.assertEqual(self.test_object.bottom, self.y + self.h)

        self.assertEqual(self.test_object.area, self.w * self.h)

    def test_get_property(self):
        self.check_property()

    def test_set_left(self):
        ox = self.x
        self.x /= 2
        self.w += ox - self.x
        self.test_object.left = self.x
        self.check_property()

    def test_set_top(self):
        oy = self.y
        self.y /= 2
        self.h += oy - self.y
        self.test_object.top = self.y
        self.check_property()

    def test_set_right(self):
        self.w *= 2
        self.test_object.right = self.x + self.w
        self.check_property()

    def test_set_bottom(self):
        self.h *= 2
        self.test_object.bottom = self.y + self.h
        self.check_property()

    def test_set_x(self):
        self.x *= 2
        self.test_object.x = self.x
        self.check_property()

    def test_set_y(self):
        self.y *= 2
        self.test_object.y = self.y
        self.check_property()

    def test_rotate(self):
        self.w, self.h = self.h, self.w
        self.test_object.rotate()
        self.check_property()

    def test_clone(self):
        cloned_object = self.test_object.clone()
        self.assertEqual(self.test_object, cloned_object)

    def test_equal(self):
        equaled_object = Rect.Rect(self.x, self.y, self.w, self.h)
        self.assertEqual(self.test_object, equaled_object)

    def test_is_overlaped(self):
        test_object = Rect.Rect(self.x, self.y, self.w, self.h)
        self.assertEqual(self.test_object.is_overlaped(test_object), True)

        test_object = Rect.Rect(self.x - self.w, self.y, self.w, self.h)
        self.assertEqual(self.test_object.is_overlaped(test_object), False)

        test_object = Rect.Rect(self.x, self.y - self.h, self.w, self.h)
        self.assertEqual(self.test_object.is_overlaped(test_object), False)


if __name__ == '__main__':
    unittest.main()
