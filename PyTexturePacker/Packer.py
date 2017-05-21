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

from .MaxRectsPacker.MaxRectsPacker import MaxRectsPacker
from .GuillotinePacker.GuillotinePacker import GuillotinePacker

TYPE_MAX_RECTS_PACK = MaxRectsPacker
TYPE_GUILLOTINE_PACK = GuillotinePacker


def create(packer_type=TYPE_MAX_RECTS_PACK, *args, **kwargs):
    """
    create a texture packer
    :param packer_type: the type of packer to create
    :param args:
    :param kwargs:
    :return:
    """
    return packer_type(*args, **kwargs)
