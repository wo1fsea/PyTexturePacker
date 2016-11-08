# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/11/06
Description:
    main_profile.py
----------------------------------------------------------------------------"""

from PyTexturePacker import Packer


def pack_test():
    packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00, trim_mode=1)
    packer.pack("test_image/", "test_image%d")


def main():
    import cProfile
    # cProfile.run("pack_test()")
    cProfile.run("pack_test()", "result")

    # >python -m cProfile myscript.py -o result

    import pstats
    p = pstats.Stats("result")
    p.strip_dirs().sort_stats(-1).print_stats()

    p.strip_dirs().sort_stats("name").print_stats()
    p.strip_dirs().sort_stats("cumulative").print_stats(10)

    p.sort_stats('tottime', 'cumtime').print_stats(.5, 'pack_test')


if __name__ == '__main__':
    main()
