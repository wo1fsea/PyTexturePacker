# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    MaxRectsPacker.py
----------------------------------------------------------------------------"""

from ..PackerInterface.PackerInterface import PackerInterface
from .MaxRectsAtlas import MaxRectsAtlas, MAX_RANK


class MaxRectsPacker(PackerInterface):
    """
    a bin packer using MaxRectsBinPack algorithm
    """

    ATLAS_TYPE = MaxRectsAtlas

    def __init__(self, *args, **kwargs):
        """
        init a MaxRectsPacker
        :param args: see PackerInterface
        """
        super(MaxRectsPacker, self).__init__(*args, **kwargs)

    def _pack(self, image_rect_list):
        atlas_list = self._init_atlas_list(image_rect_list)

        image_rect_list = sorted(image_rect_list, key=lambda x: max(
            x.width, x.height), reverse=True)

        for image_rect in image_rect_list:
            best_atlas = -1
            best_index = -1
            best_rank = MAX_RANK
            best_rotated = False

            for i, max_rect in enumerate(atlas_list):
                index, rank, rotated = max_rect.find_best_rank(
                    image_rect, self.enable_rotated)

                if rank < best_rank:
                    best_atlas = i
                    best_rank = rank
                    best_index = index
                    best_rotated = rotated

            if MAX_RANK == best_rank:
                for i, max_rect in enumerate(atlas_list):
                    while MAX_RANK == best_rank:
                        if max_rect.expand():
                            best_atlas = i
                            best_index, best_rank, best_rotated = max_rect.find_best_rank(
                                image_rect,
                                self.enable_rotated
                            )
                        else:
                            break
                    if MAX_RANK != best_rank:
                        break
                if MAX_RANK == best_rank:
                    atlas_list.append(
                        self.ATLAS_TYPE(
                            max_width=self.max_width,
                            max_height=self.max_height,
                            force_square=self.force_square,
                            border_padding=self.border_padding,
                            shape_padding=self.shape_padding,
                            inner_padding=self.inner_padding
                        )
                    )
                    best_atlas = len(atlas_list) - 1
                    best_index, best_rank, best_rotated = atlas_list[-1].find_best_rank(
                        image_rect,
                        self.enable_rotated
                    )

                    while MAX_RANK == best_rank:
                        if not atlas_list[-1].expand():
                            assert False, "can not place image [%s] in max size(%d, %d)" % (
                                image_rect.image_path,
                                self.max_width,
                                self.max_height
                            )
                        best_index, best_rank, best_rotated = atlas_list[-1].find_best_rank(
                            image_rect,
                            self.enable_rotated
                        )

            if best_rotated:
                image_rect.rotate()

            atlas_list[best_atlas].place_image_rect(best_index, image_rect)

        return atlas_list
