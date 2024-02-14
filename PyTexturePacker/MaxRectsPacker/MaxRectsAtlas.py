# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    MaxRectsAtlas.py
----------------------------------------------------------------------------"""

from ..Rect import Rect
from ..PackerInterface.AtlasInterface import AtlasInterface

MAX_RANK = 2 ** 32
MAX_WIDTH = 1024 * 16
MAX_HEIGHT = 1024 * 16


class MaxRectsAtlas(AtlasInterface):
    """
    the max rects data structure used in max rects bin pack algorithm
    """

    # EXPAND STRATEGY
    EXPAND_BOTH = 0
    EXPAND_WIDTH = 1
    EXPAND_HEIGHT = 2
    EXPAND_SHORT_SIDE = 3
    EXPAND_LONG_SIDE = 4

    # RANK STRATEGY
    RANK_BSSF = 0
    RANK_BLSF = 1
    RANK_BAF = 3

    def __init__(self, *args, **kwargs):
        super(MaxRectsAtlas, self).__init__(*args, **kwargs)

        width, height = self.size
        self.max_rect_list = [Rect(0 + self.border_padding,
                                   0 + self.border_padding,
                                   width - 2 * self.border_padding,
                                   height - 2 * self.border_padding)]

    def _is_in_max_size(self, size):
        return size[0] <= self.max_size[0] and size[1] <= self.max_size[1]

    def expand(self, method=EXPAND_SHORT_SIDE):
        if self.force_square:
            method = self.EXPAND_BOTH

        if method == MaxRectsAtlas.EXPAND_BOTH:
            new_size = (self.size[0] * 2, self.size[1] * 2)
        elif method == MaxRectsAtlas.EXPAND_WIDTH:
            new_size = (self.size[0] * 2, self.size[1])
        elif method == MaxRectsAtlas.EXPAND_HEIGHT:
            new_size = (self.size[0], self.size[1] * 2)
        elif method == MaxRectsAtlas.EXPAND_SHORT_SIDE:
            if self.size[0] <= self.size[1]:
                new_size = (self.size[0] * 2, self.size[1])
            else:
                new_size = (self.size[0], self.size[1] * 2)
        elif method == MaxRectsAtlas.EXPAND_LONG_SIDE:
            if self.size[0] >= self.size[1]:
                new_size = (self.size[0] * 2, self.size[1])
            else:
                new_size = (self.size[0], self.size[1] * 2)
        else:
            raise ValueError("Unexpected Method")

        if not self._is_in_max_size(new_size):
            return False

        old_size = self.size
        self.size = new_size

        for max_rect in self.max_rect_list:
            if max_rect.right == old_size[0] - self.border_padding:
                max_rect.right = self.size[0] - self.border_padding
            if max_rect.bottom == old_size[1] - self.border_padding:
                max_rect.bottom = self.size[1] - self.border_padding

        if old_size[0] != self.size[0]:
            new_rect = Rect(old_size[0] - self.border_padding,
                            0 + self.border_padding,
                            self.size[0] - old_size[0],
                            self.size[1] - 2 * self.border_padding)
            self.max_rect_list.append(new_rect)

        if old_size[1] != self.size[1]:
            new_rect = Rect(0 + self.border_padding,
                            old_size[1] - self.border_padding,
                            self.size[0] - 2 * self.border_padding,
                            self.size[1] - old_size[1])
            self.max_rect_list.append(new_rect)

        self.max_rect_list = list(
            filter(self._max_rect_list_pruning, self.max_rect_list))

        return True

    def cut(self, main_rect, sub_rect):
        if not main_rect.is_overlaped(sub_rect):
            return [main_rect]

        result = []
        if main_rect.left < sub_rect.left:
            tmp = main_rect.clone()
            tmp.right = sub_rect.left
            if tmp.area > 0:
                result.append(tmp)
        if main_rect.top < sub_rect.top:
            tmp = main_rect.clone()
            tmp.bottom = sub_rect.top
            if tmp.area > 0:
                result.append(tmp)
        if main_rect.right > sub_rect.right:
            tmp = main_rect.clone()
            tmp.left = sub_rect.right
            if tmp.area > 0:
                result.append(tmp)
        if main_rect.bottom > sub_rect.bottom:
            tmp = main_rect.clone()
            tmp.top = sub_rect.bottom
            if tmp.area > 0:
                result.append(tmp)

        return result

    def rank(self, main_rect, sub_rect, method=RANK_BSSF):
        """
        rank
        :param main_rect:
        :param sub_rect:
        :param method:
        :return:
        """
        if method == self.RANK_BSSF:
            tmp = main_rect.width - sub_rect.width if main_rect.width < main_rect.height \
                else main_rect.height - sub_rect.height
        elif method == self.RANK_BLSF:
            tmp = main_rect.width - sub_rect.width if main_rect.width > main_rect.height \
                else main_rect.height - sub_rect.height
        elif method == self.RANK_BAF:
            tmp = main_rect.area - sub_rect.area

        assert tmp < MAX_RANK
        if tmp < 0 \
                or main_rect.width - sub_rect.width < 2 * self.inner_padding + self.shape_padding \
                or main_rect.height - sub_rect.height < 2 * self.inner_padding + self.shape_padding:
            return MAX_RANK
        else:
            return tmp

    def find_best_rank(self, image_rect, enable_rotated=False):
        if enable_rotated:
            return self.find_best_rank_with_rotate(image_rect)
        else:
            return self.find_best_rank_without_rotate(image_rect)

    def find_best_rank_without_rotate(self, image_rect):
        best_rank = MAX_RANK
        best_index = -1
        for i, rect in enumerate(self.max_rect_list):
            rank = self.rank(rect, image_rect)
            if rank < best_rank:
                best_rank = rank
                best_index = i
        return best_index, best_rank, False

    def find_best_rank_with_rotate(self, image_rect):
        image_rect_r = image_rect.clone()
        image_rect_r.rotate()

        index, rank, _ = self.find_best_rank_without_rotate(image_rect)
        index_r, rank_r, _ = self.find_best_rank_without_rotate(image_rect_r)

        if rank < rank_r:
            return index, rank, False
        else:
            return index_r, rank, True

    def place_image_rect(self, rect_index, image_rect):
        rect = self.max_rect_list[rect_index]

        image_rect.x, image_rect.y = rect.x + \
            self.inner_padding, rect.y + self.inner_padding

        fake_image_rect = image_rect.clone()
        fake_image_rect.left -= self.inner_padding
        fake_image_rect.right += self.inner_padding + self.shape_padding
        fake_image_rect.top -= self.inner_padding
        fake_image_rect.bottom += self.inner_padding + self.shape_padding

        _max_rect_list = []
        _new_max_rect_list = []
        for i, rect in enumerate(self.max_rect_list):
            if fake_image_rect.is_overlaped(rect):
                _new_max_rect_list.extend(self.cut(rect, fake_image_rect))
            else:
                _max_rect_list.append(rect)

        self.max_rect_list = _new_max_rect_list
        self.max_rect_list = list(
            filter(self._max_rect_list_pruning, _new_max_rect_list))
        self.max_rect_list.extend(_max_rect_list)

        self.image_rect_list.append(image_rect)

    def _max_rect_list_pruning(self, rect):
        for max_rect in self.max_rect_list:
            if rect in max_rect and rect != max_rect:
                return False

        return True
