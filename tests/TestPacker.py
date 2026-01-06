import os
import unittest
from unittest.mock import Mock

from PIL import Image
from PyTexturePacker import Packer, Utils
from PyTexturePacker.ImageRect import ImageRect


# char image '!'
TEST_IMAGE_PATH = "test_image/33.png"
TEST_IMAGE_PATH2 = "test_image/129.png"
EMPTY_IMAGE_PATH = "test_image/32.png"
TEST_IMAGE_FILENAME = os.path.split(TEST_IMAGE_PATH)[1]


class TestPacker(unittest.TestCase):
    def setUp(self):
        self.save_image_mock = Mock()
        Utils.save_image = self.save_image_mock
        self.input_images = []
        Utils.load_images_from_dir = self._return_images

    def tearDown(self):
        self.save_image_mock.assert_called_once()
        self.assertEqual(len(self.atlas_data), 1)
        self.assertEqual(self.atlas_data[0]['meta']['image'], 'charset0.png')

    def _return_images(self, dir_path=None):
        return self.input_images

    def _pack(self, detect_duplicates=False, ignore_blank=False, scale=None, scale_filter=None):
        packer = Packer.create(max_width=2048, max_height=2048, border_padding=0, shape_padding=0,
            trim_mode=100, detect_duplicates=detect_duplicates, ignore_blank=ignore_blank, scale=scale,
            scale_filter=scale_filter, atlas_format=Utils.ATLAS_FORMAT_JSON)

        self.atlas_data = packer.pack("$$$", "charset%d", output_path="output", save_atlas_data=False)

    def test_detect_duplicates(self):
        image = ImageRect(TEST_IMAGE_PATH)
        image2 = image.clone()
        image3 = image.clone()
        image2.image_path = image2.image_path.replace('33', '34')
        image3.image_path = image3.image_path.replace('33', '35')
        self.input_images = [image, image2, image3]

        self._pack(detect_duplicates=True)

        self.assertEqual(len(self.atlas_data[0]['frames']), 3)

        original = self.atlas_data[0]['frames'][TEST_IMAGE_FILENAME]

        for frame in self.atlas_data[0]['frames'].values():
            self.assertEqual(frame, original)

    def test_ignore_blank(self):
        empty = ImageRect(EMPTY_IMAGE_PATH)
        emptyRgba = empty.clone()
        emptyRgba.image = emptyRgba.image.convert('RGBA')
        self.input_images = [empty, ImageRect(TEST_IMAGE_PATH), emptyRgba]

        self._pack(ignore_blank=True)

        self.assertEqual(len(self.atlas_data[0]['frames']), 1)
        self.assertIn(TEST_IMAGE_FILENAME, self.atlas_data[0]['frames'])

    def test_scale(self):
        import plistlib

        self.input_images = [ImageRect(TEST_IMAGE_PATH), ImageRect(TEST_IMAGE_PATH2)]
        original_images = list(map(lambda rect_image: (rect_image.image_path, rect_image.image.copy()), self.input_images))

        self._pack(scale=0.5, scale_filter='LANCZOS')

        self.assertEqual(len(self.atlas_data[0]['frames']), 2)
        for path, image in original_images:
            filename = os.path.split(path)[1]
            size = self.atlas_data[0]['frames'][filename]['sourceSize']
            self.assertEqual(size['w'], round(image.size[0] / 2))
            self.assertEqual(size['h'], round(image.size[1] / 2))
