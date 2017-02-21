# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    MaxRects.py
----------------------------------------------------------------------------"""

from ..Rect import Rect

MAX_RANK = 2 ** 32
MAX_WIDTH = 1024 * 16
MAX_HEIGHT = 1024 * 16


class MaxRects(object):
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

    def __init__(self, width=1, height=1, max_width=MAX_WIDTH, max_height=MAX_HEIGHT,
                 force_square=False, border_padding=0, shape_padding=0, inner_padding=0):
        super(MaxRects, self).__init__()

        if force_square:
            width = height = max(width, height)
            max_width = max_height = max(max_width, max_height)

        self.size = (width, height)
        self.max_size = (max_width, max_height)

        self.border_padding = border_padding
        self.shape_padding = shape_padding
        self.inner_padding = inner_padding

        self.force_square = force_square

        self.max_rect_list = [Rect(0 + self.border_padding,
                                   0 + self.border_padding,
                                   width - 2 * self.border_padding,
                                   height - 2 * self.border_padding)]
        self.image_rect_list = []

    def _is_in_max_size(self, size):
        return size[0] <= self.max_size[0] and size[1] <= self.max_size[1]

    def expand(self, method=EXPAND_SHORT_SIDE):
        if self.force_square:
            method = self.EXPAND_BOTH

        if method == MaxRects.EXPAND_BOTH:
            new_size = (self.size[0] * 2, self.size[1] * 2)
        elif method == MaxRects.EXPAND_WIDTH:
            new_size = (self.size[0] * 2, self.size[1])
        elif method == MaxRects.EXPAND_HEIGHT:
            new_size = (self.size[0], self.size[1] * 2)
        elif method == MaxRects.EXPAND_SHORT_SIDE:
            if self.size[0] <= self.size[1]:
                new_size = (self.size[0] * 2, self.size[1])
            else:
                new_size = (self.size[0], self.size[1] * 2)
        elif method == MaxRects.EXPAND_LONG_SIDE:
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

        self.max_rect_list = list(filter(self._max_rect_list_pruning, self.max_rect_list))

        return True

    def cut(self, main_rect, sub_rect):
        sub_rect = sub_rect.clone()
        sub_rect.left -= self.inner_padding
        sub_rect.right += self.inner_padding + self.shape_padding
        sub_rect.top -= self.inner_padding
        sub_rect.bottom += self.inner_padding + self.shape_padding

        if not main_rect.is_overlaped(sub_rect):
            return [main_rect, ]

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
        image_rect.x, image_rect.y = rect.x + self.inner_padding, rect.y + self.inner_padding

        _max_rect_list = []
        _new_max_rect_list = []
        for i, rect in enumerate(self.max_rect_list):
            if image_rect.is_overlaped(rect):
                _new_max_rect_list.extend(self.cut(rect, image_rect))
            else:
                _max_rect_list.append(rect)

        self.max_rect_list = _new_max_rect_list
        self.max_rect_list = list(filter(self._max_rect_list_pruning, _new_max_rect_list))
        self.max_rect_list.extend(_max_rect_list)

        self.image_rect_list.append(image_rect)

    def _max_rect_list_pruning(self, rect):
        for max_rect in self.max_rect_list:
            if rect in max_rect and rect != max_rect:
                return False

        return True

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
