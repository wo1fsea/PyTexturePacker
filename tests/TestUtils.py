# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/11/13
Description:
    TestUtils.py
----------------------------------------------------------------------------"""

import unittest
from PIL import Image
from PyTexturePacker import Utils

# char image '!'
TEST_IMAGE_PATH = "test_image/33.png"


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def _count_pixel_alpha_below(image, v):
        image = image.copy()
        width, height = image.size
        if image.mode != "RGBA":
            image = image.convert("RGBA")

        alpha_below_v_count = 0
        pa = image.load()
        for x in range(width):
            for y in range(height):
                pixel = pa[x, y]
                if pixel[3] < v:
                    alpha_below_v_count += 1

        return alpha_below_v_count

    def test_alpha_remove(self):
        image = Image.open(TEST_IMAGE_PATH)

        alpha_zero_count = self._count_pixel_alpha_below(image, 1)
        self.assertGreater(alpha_zero_count, 0)

        image = Utils.alpha_remove(image)
        alpha_zero_count = self._count_pixel_alpha_below(image, 1)
        self.assertEqual(alpha_zero_count, 0)

    def test_clean_pixel_alpha_below(self):
        image = Image.open(TEST_IMAGE_PATH)

        v1 = 1
        alpha_below_v1_count = self._count_pixel_alpha_below(image, v1)

        v2 = 256
        alpha_below_v2_count = self._count_pixel_alpha_below(image, v2)

        self.assertGreater(alpha_below_v2_count - alpha_below_v1_count, 0)

        image = Utils.clean_pixel_alpha_below(image, v2)

        alpha_below_v1_count = self._count_pixel_alpha_below(image, v1)
        alpha_below_v2_count = self._count_pixel_alpha_below(image, v2)

        self.assertEqual(alpha_below_v2_count - alpha_below_v1_count, 0)