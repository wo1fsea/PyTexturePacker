# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    main.py
----------------------------------------------------------------------------"""

from PyTexturePacker import Packer


def pack_test():
    # create a MaxRectsBinPacker
    packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00)
    # pack texture images under the directory "test_case/" and name the output images as "test_case".
    # "%d" in output file name "test_case%d" is a placeholder, which is a multipack index, starting with 0.
    packer.pack("test_image/", "test_image%d")


def main():
    pack_test()


if __name__ == '__main__':
    main()
