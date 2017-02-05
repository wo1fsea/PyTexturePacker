# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    ImageRect.py
----------------------------------------------------------------------------"""

from PIL import Image

from .Rect import Rect
from . import Utils

class ImageRect(Rect):
    """
    image rect data
    """

    def __init__(self, image_path=None):
        super(ImageRect, self).__init__(0, 0, 0, 0)

        self.image = None
        self.image_path = None
        self.source_size = (0, 0)
        self.source_box = (0, 0, 0, 0)

        self._rotated = False
        self._trimmed = False
        if image_path:
            self.load_image(image_path)
            self.image_path = image_path

    @property
    def rotated(self):
        return self._rotated

    @property
    def trimmed(self):
        return self._trimmed

    @property
    def bbox(self):
        if self._trimmed:
            return self.image.getbbox()
        else:
            return tuple(0, 0, self.width, self.height)

    def load_image(self, image_path):
        image = Image.open(image_path)
        self.image = image.copy()
        image.close()

        self.image_path = image_path

        self.x, self.y = 0, 0
        self.width, self.height = self.image.size

        self.source_size = self.image.size
        self.source_box = (0, 0, self.width, self.height)

        self._rotated = False
        self._trimmed = False

    def rotate(self):
        self._rotated = not self._rotated

        width = self.width
        self.width = self.height
        self.height = width

    def trim(self, v=1):
        if self._trimmed:
            return

        self.image = Utils.clean_pixel_alpha_below(self.image, v)
        bbox = self.image.getbbox()
        if bbox:
            self.image = self.image.crop(bbox)
            self.source_box = bbox
            self.width, self.height = self.image.size

        self._trimmed = True

    def clone(self):
        tmp = ImageRect()

        tmp.image = self.image
        tmp.image_path = self.image_path

        tmp.x, tmp.y = self.x, self.y
        tmp.width, tmp.height = self.width, self.height

        tmp.source_size = self.source_size
        tmp.source_box = self.source_box

        tmp._rotated = self._rotated
        tmp._trimmed = self._trimmed
        return tmp


def main():
    img_rect = ImageRect("test.jpg")
    img_rect.rotate()


if __name__ == '__main__':
    main()
