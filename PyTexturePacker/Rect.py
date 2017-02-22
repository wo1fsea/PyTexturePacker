# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    Rect.py
----------------------------------------------------------------------------"""


class Rect(object):
    """
    rect type data

    (left, top)
            +----+
            |    |
            +----+
                (right, bottom)
    """

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.width, self.height = w, h

    @property
    def left(self):
        return self.x

    @left.setter
    def left(self, value):
        self.width = self.right - value
        self.x = value

    @property
    def top(self):
        return self.y

    @top.setter
    def top(self, value):
        self.height = self.bottom - value
        self.y = value

    @property
    def right(self):
        return self.x + self.width

    @right.setter
    def right(self, value):
        self.width = value - self.left

    @property
    def bottom(self):
        return self.y + self.height

    @bottom.setter
    def bottom(self, value):
        self.height = value - self.top

    @property
    def area(self):
        return self.width * self.height

    def clone(self):
        return Rect(self.x, self.y, self.width, self.height)

    def is_overlaped(self, rect):
        return not (self.x >= rect.x + rect.width or
                    self.y >= rect.y + rect.height or
                    self.x + self.width <= rect.x or
                    self.y + self.height <= rect.y)

    def __contains__(self, rect):
        return (self.x <= rect.x and
                self.y <= rect.y and
                self.x + self.width >= rect.x + rect.width and
                self.y + self.height >= rect.y + rect.height)

    def __ne__(self, other):
        return (self.x != other.x or
                self.y != other.y or
                self.width != other.width or
                self.height != other.height)

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.width == other.width and
                self.height == other.height)

    def rotate(self):
        width = self.width
        self.width = self.height
        self.height = width


def main():
    rect_a = Rect(0, 0, 6, 1)
    rect_b = Rect(0, 0, 5, 5)
    print(rect_a in rect_b, rect_b in rect_a)


if __name__ == '__main__':
    main()
