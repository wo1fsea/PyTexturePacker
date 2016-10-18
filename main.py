# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong
Date:
	2016/10/18
Description:
	xx
----------------------------------------------------------------------------"""

from PyTexturePacker import Packer

def main():
    packer = Packer.create(max_width=256)
    packer.pack("test_case/", "test_case")

if __name__ == '__main__':
    main()

