from Rect import Rect
from PIL import Image


class ImageRect(Rect):
    """
    Image Rect data
    """

    def __init__(self, image_path=None):
        super(ImageRect, self).__init__(0, 0, 0, 0)
        self.image = None
        self._rotated = False
        if image_path:
            self.load_image(image_path)

    @property
    def rotated(self):
        return self._rotated

    def load_image(self, image_path):
        self.image = Image.open(image_path)
        self.x, self.y = 0, 0
        self.width, self.height = self.image.size

    def rotate(self):
        # rotate = Image.ROTATE_90 if self._rotated else Image.ROTATE_270
        # self._image = self._image.transpose(rotate)
        self._rotated = not self._rotated

        width = self.width
        self.width = self.height
        self.height = width

    def clone(self):
        tmp = ImageRect()
        tmp.x, tmp.y = self.x, self.y
        tmp.width, tmp.height = self.width, self.height
        tmp.image = self.image
        tmp._rotated = self._rotated
        return tmp


def main():
    img_rect = ImageRect("test.jpg")
    img_rect.rotate()


if __name__ == '__main__':
    main()