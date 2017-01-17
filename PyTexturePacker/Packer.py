# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    Packer.py
----------------------------------------------------------------------------"""

from .MaxRectsBinPacker.MaxRectsBinPacker import MaxRectsBinPacker

TYPE_MAX_RECTS_BIN_PACK = MaxRectsBinPacker


def create(packer_type=TYPE_MAX_RECTS_BIN_PACK, *args, **kwargs):
    """
    create a texture packer
    :param packer_type: the type of packer to create
    :param args:
    :param kwargs:
    :return:
    """
    return MaxRectsBinPacker(*args, **kwargs)
