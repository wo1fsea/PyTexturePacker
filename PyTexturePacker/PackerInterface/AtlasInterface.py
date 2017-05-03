# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2017/4/26
Description:
    AtlasInterface.py
----------------------------------------------------------------------------"""

MAX_RANK = 2 ** 32
MAX_WIDTH = 1024 * 16
MAX_HEIGHT = 1024 * 16


class AtlasInterface(object):
    """
    interface of atlas
    """

    def __init__(self, width=1, height=1, max_width=MAX_WIDTH, max_height=MAX_HEIGHT,
                 force_square=False, border_padding=0, shape_padding=0, inner_padding=0):
        if force_square:
            width = height = max(width, height)
            max_width = max_height = max(max_width, max_height)

        self.size = (width, height)
        self.max_size = (max_width, max_height)

        self.border_padding = border_padding
        self.shape_padding = shape_padding
        self.inner_padding = inner_padding

        self.force_square = force_square

        self.image_rect_list = []

    def dump_plist(self, texture_file_name="", input_base_path=None):
        import os

        plist_data = {}

        frames = {}
        for image_rect in self.image_rect_list:
            width, height = (image_rect.width, image_rect.height) if not image_rect.rotated \
                else (image_rect.height, image_rect.width)

            center_offset = (0, 0)
            if image_rect.trimmed:
                center_offset = (image_rect.source_box[0] + width / 2. - image_rect.source_size[0] / 2.,
                                 - (image_rect.source_box[1] + height / 2. - image_rect.source_size[1] / 2.))

            path = image_rect.image_path
            if input_base_path is None:
                _, path = os.path.split(path)
            else:
                path = os.path.relpath(os.path.abspath(path), os.path.abspath(input_base_path))

            frames[path] = dict(
                frame="{{%d,%d},{%d,%d}}" % (image_rect.x, image_rect.y, width, height),
                offset="{%d,%d}" % center_offset,
                rotated=bool(image_rect.rotated),
                sourceColorRect="{{%d,%d},{%d,%d}}" % (
                    image_rect.source_box[0], image_rect.source_box[1], width, height),
                sourceSize="{%d,%d}" % image_rect.source_size,
            )

        plist_data["frames"] = frames
        plist_data["metadata"] = dict(
            format=int(2),
            textureFileName=texture_file_name,
            realTextureFileName=texture_file_name,
            size="{%d,%d}" % self.size,
        )

        return plist_data

    def dump_image(self, bg_color=0xffffffff):
        from PIL import Image
        packed_image = Image.new('RGBA', self.size, bg_color)

        for image_rect in self.image_rect_list:
            image = image_rect.image.crop()
            if image_rect.rotated:
                image = image.transpose(Image.ROTATE_270)
            packed_image.paste(image, (image_rect.left, image_rect.top, image_rect.right, image_rect.bottom))

        return packed_image
