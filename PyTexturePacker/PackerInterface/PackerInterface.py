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

	def __init__(self, bg_color=0x00000000, texture_format=".png", max_width=4096, max_height=4096, enable_rotated=True,
				 force_square=False, border_padding=2, shape_padding=2, inner_padding=0, trim_mode=0,
				 reduce_border_artifacts=False):
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
		self.trim_mode = trim_mode
		self.reduce_border_artifacts = reduce_border_artifacts

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

		atlas_list = self._pack(image_rects)

		assert "%d" in output_name or len(atlas_list) == 1, 'more than one output image, but no "%d" in output_name'

		for i, atlas in enumerate(atlas_list):
			texture_file_name = output_name if "%d" not in output_name else output_name % i

			packed_plist = atlas.dump_plist("%s%s" % (texture_file_name, self.texture_format), input_base_path)
			packed_image = atlas.dump_image(self.bg_color)

			if self.reduce_border_artifacts:
				packed_image = Utils.alpha_bleeding(packed_image)

			Utils.save_plist(packed_plist, os.path.join(output_path, "%s.plist" % texture_file_name))
			Utils.save_image(packed_image, os.path.join(output_path, "%s%s" % (texture_file_name, self.texture_format)))

	def multi_pack(self, pack_args_list):
		"""
		pack with multiprocessing
		:param pack_args_list: list of pack args
		:return:
		"""

		import multiprocessing

		pool_size = multiprocessing.cpu_count() * 2
		pool = multiprocessing.Pool(processes=pool_size)

		pool.map(multi_pack_handler, zip([self] * len(pack_args_list), pack_args_list))
		pool.close()
		pool.join()
