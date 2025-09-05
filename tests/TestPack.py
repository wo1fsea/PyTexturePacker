'''
 # @ Author: hui.xie
 # @ Create Time: 2025-09-05 16:02:21
 # @ Modified by: hui.xie
 # @ Modified time: 2025-09-05 16:05:34
 # @ Description:
 '''


import unittest
from PyTexturePacker import Packer

TEST_IMAGE_DIR = 'test_pack_image'
TEST_PLIST_DIR = 'test_pack_image/output/test'

class TestRect(unittest.TestCase):
    def setUp(self):
        self.test_dir = TEST_IMAGE_DIR
        self.test_out = TEST_PLIST_DIR

    def tearDown(self):
        pass

    def test_pack(self):
        packer = Packer.create(max_width=4096, max_height=4096, bg_color=0x00000000, border_padding=2,
                               shape_padding=2, extrude=0, trim_mode=1, enable_rotated=True, trim_sprite_names=True)
        print('Packing textures...')
        packer.pack(self.test_dir, self.test_out, input_base_path=self.test_dir)
        print('Packing completed.')


if __name__ == '__main__':
    unittest.main()