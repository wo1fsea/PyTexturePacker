# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong (wo1fSea)
	quanyongh@foxmail.com
Date:
	2016/10/18
Description:
	Rect
----------------------------------------------------------------------------"""


class Rect(object):
	"""
	Rect type data

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
		return not (self.left >= rect.right or
					self.top >= rect.bottom or
					self.right <= rect.left or
					self.bottom <= rect.top)

	def __contains__(self, rect):
		return (self.left <= rect.left and
				self.top <= rect.top and
				self.right >= rect.right and
				self.bottom >= rect.bottom)

	def __ne__(self, other):
		return not self == other

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
