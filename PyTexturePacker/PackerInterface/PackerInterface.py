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

import os

from .. import Utils
from .AtlasInterface import AtlasInterface

SIZE_SEQUENCE = [2 ** ind for ind in range(32)]


def multi_pack_handler(args):
    packer, args = args

    if isinstance(args, (list, tuple)):
        packer.pack(*args)
    elif isinstance(args, dict):
        packer.pack(**args)


class PackerInterface(object):
    """
    interface of packer
    """
    ATLAS_TYPE = AtlasInterface

    def __init__(self, bg_color=0x00000000, texture_format=".png", max_width=4096, max_height=4096, enable_rotated=True,
                 force_square=False, border_padding=2, shape_padding=2, inner_padding=0, trim_mode=0,
                 reduce_border_artifacts=False, extrude=0, atlas_format=Utils.ATLAS_FORMAT_PLIST, atlas_ext=None):
        """
        init a packer
        :param bg_color: background color of output image.
        :param texture_format: texture format of the output file
        :param max_width: the maximum width
        :param max_height: the maximum height
        :param enable_rotated: allow the rotating of sprites if there is a better fit in the texture
        :param force_square: forces the texture to have a squared size
        :param border_padding: space between the sprites and the border of the sprite sheet
        :param shape_padding: space between sprites
        :param inner_padding: adds transparent pixels to the inside of the sprite, growing it
        :param trim_mode: pixels with an alpha value below this value will be trimmed. when 0, disable
        :param reduce_border_artifacts: adds color to transparent pixels by repeating a sprite's outer color values
        :param extrude: extrude repeats the sprite's pixels at the border. Sprite's size is not changed.
        :param atlas_format: texture config output type: 'plist' or 'json'. default: 'plist'
        """

        self.bg_color = bg_color
        self.texture_format = texture_format
        self.max_width = max_width
        self.max_height = max_height
        self.enable_rotated = enable_rotated
        self.force_square = force_square
        self.border_padding = border_padding
        self.shape_padding = shape_padding
        self.inner_padding = inner_padding
        self.extrude = extrude
        self.trim_mode = trim_mode
        self.reduce_border_artifacts = reduce_border_artifacts
        self.atlas_format = atlas_format
        self.atlas_ext = atlas_ext

    @staticmethod
    def _calculate_area(image_rect_list, inner_padding):
        area = 0
        for image_rect in image_rect_list:
            area += image_rect.area + \
                image_rect.width * inner_padding + \
                image_rect.height * inner_padding + \
                inner_padding ** 2
        return area

    @staticmethod
    def _cal_init_size(area, min_width, min_height, max_width, max_height):
        min_short = min(min_width, min_height)
        min_long = max(min_width, min_height)

        max_short = min(max_width, max_height)
        max_long = max(max_width, max_height)

        start_i = -1
        start_j = -1

        for i, l in enumerate(SIZE_SEQUENCE):
            if l >= min_short and start_i == -1:
                start_i = i
            if l >= min_long and start_j == -1:
                start_j = i

        short = -1
        long = -1

        for j in range(start_j, len(SIZE_SEQUENCE)):
            l = SIZE_SEQUENCE[j]
            if (short != -1 and long != -1) or l > max_long:
                break

            for i in range(start_i, j + 1):
                s = SIZE_SEQUENCE[i]
                if (short != -1 and long != -1) or s > max_short:
                    break

                if area <= l * s:
                    short, long = s, l

        if short == -1 and long == -1:
            return tuple((max_height, max_width))

        if min_width == min_long:
            return tuple((long, short))
        else:
            return tuple((short, long))

    def _init_atlas_list(self, image_rect_list):
        min_width, min_height = 0, 0
        for image_rect in image_rect_list:
            if min_width < image_rect.width:
                min_width = image_rect.width
            if min_height < image_rect.height:
                min_height = image_rect.height

        min_width += self.inner_padding
        min_height += self.inner_padding

        if self.enable_rotated:
            if min(min_width, min_height) > min(self.max_width, self.max_height) or \
                    max(min_width, min_height) > max(self.max_width, self.max_height):
                raise ValueError("size of image is larger than max size.")
        else:
            if min_height > self.max_height or min_width > self.max_width:
                raise ValueError("size of image is larger than max size.")

        atlas_list = []
        area = self._calculate_area(image_rect_list, self.inner_padding)
        w, h = self._cal_init_size(
            area, min_width, min_height, self.max_width, self.max_height)

        atlas_list.append(self.ATLAS_TYPE(w, h, self.max_width, self.max_height,
                                          force_square=self.force_square, border_padding=self.border_padding,
                                          shape_padding=self.shape_padding, inner_padding=self.inner_padding))

        area = area - w * h
        while area > 0:
            w, h = self._cal_init_size(
                area, 0, 0, self.max_width, self.max_height)
            area = area - w * h
            atlas_list.append(self.ATLAS_TYPE(w, h, self.max_width, self.max_height,
                                              force_square=self.force_square, border_padding=self.border_padding,
                                              shape_padding=self.shape_padding, inner_padding=self.inner_padding))

        return atlas_list

    def _pack(self, image_rect_list):
        raise NotImplementedError

    def pack(self, input_images, output_name, output_path="", input_base_path=None):
        """
        pack the input images to sheets
        :param input_images: a list of input image paths or a input dir path
        :param output_name: the output file name
        :param output_path: the output file path
        :param input_base_path: the base path of input files
        :return:
        """

        if isinstance(input_images, (tuple, list)):
            image_rects = Utils.load_images_from_paths(input_images)
        else:
            image_rects = Utils.load_images_from_dir(input_images)

        if self.trim_mode:
            for image_rect in image_rects:
                image_rect.trim(self.trim_mode)

        if self.extrude:
            for image_rect in image_rects:
                image_rect.extrude(self.extrude)

        atlas_list = self._pack(image_rects)

        assert "%d" in output_name or len(
            atlas_list) == 1, 'more than one output image, but no "%d" in output_name'

        for i, atlas in enumerate(atlas_list):
            texture_file_name = output_name if "%d" not in output_name else output_name % i

            packed_plist = atlas.dump_plist("%s%s" % (texture_file_name, self.texture_format), input_base_path,
                                            self.atlas_format)
            packed_image = atlas.dump_image(self.bg_color)

            if self.reduce_border_artifacts:
                packed_image = Utils.alpha_bleeding(packed_image)

            atlas_data_ext = self.atlas_ext or Utils.get_atlas_data_ext(
                self.atlas_format)
            Utils.save_atlas_data(packed_plist, os.path.join(output_path, "%s%s" % (texture_file_name, atlas_data_ext)),
                                  self.atlas_format)
            Utils.save_image(packed_image, os.path.join(
                output_path, "%s%s" % (texture_file_name, self.texture_format)))

    def multi_pack(self, pack_args_list):
        """
        pack with multiprocessing
        :param pack_args_list: list of pack args
        :return:
        """

        import multiprocessing

        pool_size = multiprocessing.cpu_count() * 2
        pool = multiprocessing.Pool(processes=pool_size)

        pool.map(multi_pack_handler, zip(
            [self] * len(pack_args_list), pack_args_list))
        pool.close()
        pool.join()
