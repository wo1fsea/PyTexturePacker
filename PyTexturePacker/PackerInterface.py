# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    PackerInterface.py
----------------------------------------------------------------------------"""


class PackerInterface(object):
    """
    """

    def __init__(self, bg_color=0x00000000, texture_format=".png", max_width=4096, max_height=4096, enable_rotated=True,
                 force_square=False, shape_padding=0, reduce_border_artifacts=False):
        """

        :param bg_color:
        :param texture_format:
        :param max_width:
        :param max_height:
        :param enable_rotated:
        :param force_square:
        :param shape_padding:
        :param reduce_border_artifacts:
        """
        self.bg_color = bg_color
        self.texture_format = texture_format
        self.max_width = max_width
        self.max_height = max_height
        self.enable_rotated = enable_rotated
        self.force_square = force_square
        self.shape_padding = shape_padding
        self.reduce_border_artifacts = reduce_border_artifacts

    def pack(self, input_images, output_name, output_path=""):
        raise NotImplementedError
