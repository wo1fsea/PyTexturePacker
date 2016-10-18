# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong (wo1fSea)
	quanyongh@foxmail.com
Date:
	2016/10/18
Description:
	MaxRectsBinPacker
----------------------------------------------------------------------------"""

import os

from .. import Utils
from ..PackerInterface import PackerInterface
from .MaxRects import MaxRects, MAX_RANK

SIZE_SEQUENCE = [2 ** ind for ind in range(32)]


def calculate_area(image_rect_list):
	area = 0
	for image_rect in image_rect_list:
		area += image_rect.area
	return area


def cal_init_size(area, min_side_len=0, max_side_len=SIZE_SEQUENCE[-1], force_square=False):
	start_i = 0

	for i, l in enumerate(SIZE_SEQUENCE):
		if l >= min_side_len:
			start_i = i
			break

	if force_square:
		for i, l in enumerate(SIZE_SEQUENCE):
			if i < start_i:
				continue
			if area <= l * l:
				return tuple((l if l < max_side_len else max_side_len, l if l < max_side_len else max_side_len))
	else:
		for i, l in enumerate(SIZE_SEQUENCE):
			if i < start_i:
				continue
			for j in range(0, i + 1):
				l2 = SIZE_SEQUENCE[j]
				if area <= l * l2:
					return tuple((l if l < max_side_len else max_side_len, l2 if l2 < max_side_len else max_side_len))

	return tuple((max_side_len, max_side_len))


class MaxRectsBinPacker(PackerInterface):
	"""

	"""

	def __init__(self, *args, **kwargs):
		"""

		:param args:
		"""
		super(MaxRectsBinPacker, self).__init__(*args, **kwargs)

	def pack(self, input_images, output_name, output_path=""):
		"""

		:param input_images:
		:param output_name:
		:param output_path:
		:return:
		"""

		if isinstance(input_images, (tuple, list)):
			image_rects = Utils.load_images_from_paths(input_images)
		else:
			image_rects = Utils.load_images_from_dir(input_images)

		max_rect_list = self._pack(image_rects, self.max_width)

		output_plist_list = []
		output_image_list = []

		for i, max_rect in enumerate(max_rect_list):
			packed_image = max_rect.dump_image(self.bg_color)
			packed_plist = max_rect.dump_plist()

			output_image_list.append(packed_image)
			output_plist_list.append(packed_plist)

		if len(output_plist_list) == 1:
			Utils.save_plist(output_plist_list[0], os.path.join(output_path, "%s.plist" % output_name))
			Utils.save_image(output_image_list[0], os.path.join(output_path, "%s.png" % output_name))
		else:
			for i, plist in enumerate(output_plist_list):
				Utils.save_plist(plist, os.path.join(output_path, "%s%d.plist" % (output_name, i)))
			for i, image in enumerate(output_image_list):
				Utils.save_image(image, os.path.join(output_path, "%s%d%s" % (output_name, i, self.texture_format)))

	def _pack(self, image_rect_list, max_size):
		min_size = 0
		for image_rect in image_rect_list:
			tmp = max(image_rect.width, image_rect.height)
			if tmp > min_size:
				min_size = tmp

		if min_size > max_size:
			raise ValueError("size of image is larger than max_size.")

		max_rects_list = []

		area = calculate_area(image_rect_list)
		w, h = cal_init_size(area, min_size, max_size)

		max_rects_list.append(MaxRects(w, h))

		area = area - w * h
		while area > 0:
			w, h = cal_init_size(area, max_side_len=max_size)
			area = area - w * h
			max_rects_list.append(MaxRects(w, h))

		image_rect_list = sorted(image_rect_list, key=lambda x: max(x.width, x.height), reverse=True)

		for image_rect in image_rect_list:
			best_max_rects = -1
			best_index = -1
			best_rank = MAX_RANK
			best_rotated = False

			for i, max_rect in enumerate(max_rects_list):
				index, rank, rotated = max_rect.find_best_rank_with_rotate(image_rect)

				if rank < best_rank:
					best_max_rects = i
					best_rank = rank
					best_index = index
					best_rotated = rotated

			if MAX_RANK == best_rank:
				for i, max_rect in enumerate(max_rects_list):
					while MAX_RANK == best_rank:
						if max_rect.size[0] <= max_size / 2 or max_rect.size[1] <= max_size / 2:
							max_rect.expand(MaxRects.EXPAND_SHORT_SIDE)
							best_max_rects = i
							best_index, best_rank, best_rotated = max_rect.find_best_rank_with_rotate(image_rect)
						else:
							break
					if MAX_RANK != best_rank:
						break
				if MAX_RANK == best_rank:
					max_rects_list.append(MaxRects())
					best_max_rects = len(max_rects_list) - 1
					best_index, best_rank, best_rotated = max_rects_list[-1].find_best_rank_with_rotate(image_rect)
					while MAX_RANK == best_rank:
						max_rects_list[-1].expand(MaxRects.EXPAND_SHORT_SIDE)
						best_index, best_rank, best_rotated = max_rects_list[-1].find_best_rank_with_rotate(image_rect)

			if best_rotated:
				image_rect.rotate()

			max_rects_list[best_max_rects].place_image_rect(best_index, image_rect)

		return max_rects_list
