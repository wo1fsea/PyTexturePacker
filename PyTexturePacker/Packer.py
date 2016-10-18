# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong (wo1fSea)
	quanyongh@foxmail.com
Date:
	2016/10/18
Description:
	Packer
----------------------------------------------------------------------------"""

from .MaxRectsBinPacker.MaxRectsBinPacker import MaxRectsBinPacker

TYPE_MAX_RECTS_BIN_PACK = MaxRectsBinPacker


def create(packer_type=TYPE_MAX_RECTS_BIN_PACK, *args, **kwargs):
	return MaxRectsBinPacker(*args, **kwargs)
