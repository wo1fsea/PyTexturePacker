# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    GuillotinePacker.py
----------------------------------------------------------------------------"""

from ..MaxRectsPacker.MaxRectsPacker import MaxRectsPacker
from ..GuillotinePacker.GuillotineAtlas import GuillotineAtlas


class GuillotinePacker(MaxRectsPacker):
    """
    a bin packer using guillotine algorithm
    """

    ATLAS_TYPE = GuillotineAtlas
