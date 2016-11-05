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
    packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00, trim_mode=1)
    packer.pack("test_image/", "test_image%d")


def main():
    pack_test()


if __name__ == '__main__':
    main()
