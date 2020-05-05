# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/11/10
Description:
    TestImageRect.py
----------------------------------------------------------------------------"""

import unittest
from PIL import Image
from PyTexturePacker import ImageRect

# char image '!'
TEST_IMAGE_PATH = "test_image/33.png"


class TestImageRect(unittest.TestCase):
    def setUp(self):
        self.test_object = ImageRect.ImageRect(TEST_IMAGE_PATH)
        self.pil_image_object = Image.open(TEST_IMAGE_PATH)

    def tearDown(self):
        pass

    def check_equal(self, object):
        self.assertEqual(self.test_object.image_path, object.image_path)

        self.assertEqual(self.test_object.x, object.x)
        self.assertEqual(self.test_object.y, object.y)

        self.assertEqual(self.test_object.width, object.width)
        self.assertEqual(self.test_object.height, object.height)

        self.assertEqual(self.test_object.source_size[0], object.source_size[0])
        self.assertEqual(self.test_object.source_size[1], object.source_size[1])

        self.assertEqual(self.test_object.source_box[0], object.source_box[0])
        self.assertEqual(self.test_object.source_box[1], object.source_box[1])
        self.assertEqual(self.test_object.source_box[2], object.source_box[2])
        self.assertEqual(self.test_object.source_box[3], object.source_box[3])

        self.assertEqual(self.test_object.trimmed, object.trimmed)
        self.assertEqual(self.test_object.rotated, object.rotated)

    def test_clone(self):
        clone_object = self.test_object.clone()
        self.check_equal(clone_object)

    def test_properties(self):
        self.test_object = ImageRect.ImageRect(TEST_IMAGE_PATH)

        self.assertEqual(self.test_object.image_path, TEST_IMAGE_PATH)

        self.assertEqual(self.test_object.width, self.pil_image_object.size[0])
        self.assertEqual(self.test_object.height, self.pil_image_object.size[1])

        self.assertEqual(self.test_object.x, 0)
        self.assertEqual(self.test_object.y, 0)

        self.assertEqual(self.test_object.source_size[0], self.pil_image_object.size[0])
        self.assertEqual(self.test_object.source_size[1], self.pil_image_object.size[1])

        self.assertEqual(self.test_object.source_box[0], 0)
        self.assertEqual(self.test_object.source_box[1], 0)
        self.assertEqual(self.test_object.source_box[2], self.pil_image_object.size[0])
        self.assertEqual(self.test_object.source_box[3], self.pil_image_object.size[1])

        self.assertEqual(self.test_object.rotated, False)
        self.assertEqual(self.test_object.trimmed, False)

    def test_trim(self):
        bbox = self.pil_image_object.getbbox()

        self.test_object.trim()

        self.assertSequenceEqual(self.test_object.source_box, bbox)

        self.assertEqual(self.test_object.width, bbox[2] - bbox[0])
        self.assertEqual(self.test_object.height, bbox[3] - bbox[1])

        self.assertEqual(self.test_object.trimmed, True)

    def test_extrude(self):
        test_object = ImageRect.ImageRect("test_image/128.png")
        pil_image_object = Image.open("test_image/129.png")
        test_object.extrude(1)

        self.assertEqual(test_object.extrude_size, 1)
        self.assertEqual(test_object.width, pil_image_object.size[0])
        self.assertEqual(test_object.height, pil_image_object.size[1])

        for x in range(test_object.image.size[0]):
            for y in range(test_object.image.size[1]):
                self.assertSequenceEqual(pil_image_object.getpixel((x, y)), test_object.image.getpixel((x, y)))
