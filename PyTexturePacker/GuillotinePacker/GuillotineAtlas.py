# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    GuillotineAtlas.py
----------------------------------------------------------------------------"""

from ..Rect import Rect
from ..MaxRectsPacker.MaxRectsAtlas import MaxRectsAtlas

MAX_RANK = 2 ** 32
MAX_WIDTH = 1024 * 16
MAX_HEIGHT = 1024 * 16


class GuillotineAtlas(MaxRectsAtlas):
    """
    the guillotine rects data structure used in guillotine algorithm
    """

    def cut(self, main_rect, sub_rect):
        result = [Rect(main_rect.left, main_rect.top,
                       sub_rect.left - main_rect.left, sub_rect.top - main_rect.top),
                  Rect(sub_rect.left, main_rect.top,
                       sub_rect.width, sub_rect.top - main_rect.top),
                  Rect(sub_rect.right, main_rect.top,
                       main_rect.right - sub_rect.right, sub_rect.top - main_rect.top),

                  Rect(main_rect.left, sub_rect.top,
                       sub_rect.left - main_rect.left, sub_rect.height),
                  # Rect(sub_rect.left, sub_rect.top,
                  #     sub_rect.width, sub_rect.height),
                  Rect(sub_rect.right, sub_rect.top,
                       main_rect.right - sub_rect.right, sub_rect.height),

                  Rect(main_rect.left, sub_rect.bottom,
                       sub_rect.left - main_rect.left, main_rect.bottom - sub_rect.bottom),
                  Rect(sub_rect.left, sub_rect.bottom,
                       sub_rect.width, main_rect.bottom - sub_rect.bottom),
                  Rect(sub_rect.right, sub_rect.bottom,
                       main_rect.right - sub_rect.right, main_rect.bottom - sub_rect.bottom),
                  ]

        return filter(lambda rect: rect.area > 0, result)

    def place_image_rect(self, rect_index, image_rect):
        rect = self.max_rect_list[rect_index]

        image_rect.x, image_rect.y = rect.x + \
            self.inner_padding, rect.y + self.inner_padding

        fake_image_rect = image_rect.clone()
        fake_image_rect.left -= self.inner_padding
        fake_image_rect.right += self.inner_padding + self.shape_padding
        fake_image_rect.top -= self.inner_padding
        fake_image_rect.bottom += self.inner_padding + self.shape_padding

        self.max_rect_list.pop(rect_index)
        self.max_rect_list.extend(self.cut(rect, fake_image_rect))
        self.image_rect_list.append(image_rect)
