import math
import sys
from Rect import Rect

MAX_RANK = 2 ** 32
SIZE_SEQUENCE = [2**ind for ind in range(32)]


class MaxRects(object):
    """
    the max rects data
    """

    EXPAND_BOTH = 0
    EXPAND_WIDTH = 1
    EXPAND_HEIGHT = 2
    EXPAND_SHORT_SIDE = 3
    EXPAND_LONG_SIDE = 4

    def __init__(self, width=1, height=1):
        self.size = (width, height)

        self.max_rect_list = [Rect(0, 0, width, height)]
        self.image_rect_list = []

    def expand(self, method=EXPAND_BOTH):
        old_size = self.size
        if method == MaxRects.EXPAND_BOTH:
            self.size = (self.size[0] * 2, self.size[1] * 2)
        elif method == MaxRects.EXPAND_WIDTH:
            self.size = (self.size[0] * 2, self.size[1])
        elif method == MaxRects.EXPAND_HEIGHT:
            self.size = (self.size[0], self.size[1] * 2)
        elif method == MaxRects.EXPAND_SHORT_SIDE:
            if self.size[0] <= self.size[1]:
                self.size = (self.size[0] * 2, self.size[1])
            else:
                self.size = (self.size[0], self.size[1] * 2)
        elif method == MaxRects.EXPAND_LONG_SIDE:
            if self.size[0] >= self.size[1]:
                self.size = (self.size[0] * 2, self.size[1])
            else:
                self.size = (self.size[0], self.size[1] * 2)
        else:
            raise ValueError("Unexpected Method")

        for max_rect in self.max_rect_list:
            if max_rect.right == old_size[0]:
                max_rect.right = self.size[0]
            if max_rect.bottom == old_size[1]:
                max_rect.bottom = self.size[1]

        if old_size[0] != self.size[0]:
            new_rect = Rect(old_size[0], 0, self.size[0] - old_size[0], self.size[1])
            self.max_rect_list.append(new_rect)

        if old_size[1] != self.size[1]:
            new_rect = Rect(0, old_size[1], self.size[0], self.size[1] - old_size[1])
            self.max_rect_list.append(new_rect)

        self.max_rect_list = filter(self._max_rect_list_pruning, self.max_rect_list)

    def cut(self, main_rect, sub_rect):
        if not main_rect.is_overlaped(sub_rect):
            return [main_rect, ]

        result = []
        if main_rect.left < sub_rect.left:
            tmp = main_rect.clone()
            tmp.right = sub_rect.left# - 1
            result.append(tmp)
        if main_rect.top < sub_rect.top:
            tmp = main_rect.clone()
            tmp.bottom = sub_rect.top# - 1
            result.append(tmp)
        if main_rect.right > sub_rect.right:
            tmp = main_rect.clone()
            tmp.left = sub_rect.right# + 1
            result.append(tmp)
        if main_rect.bottom > sub_rect.bottom:
            tmp = main_rect.clone()
            tmp.top = sub_rect.bottom# + 1
            result.append(tmp)

        return result

    def rank(self, main_rect, sub_rect):
        """
        BSSF
        :param main_rect:
        :param sub_rect:
        :return:
        """
        tmp = min(main_rect.width - sub_rect.width, main_rect.height - sub_rect.height)
        assert tmp < MAX_RANK
        if tmp < 0:
            return MAX_RANK
        else:
            return tmp

    def find_best_rank(self, image_rect):
        best_rank = MAX_RANK
        best_index = -1
        for i, rect in enumerate(self.max_rect_list):
            rank = self.rank(rect, image_rect)
            if rank < best_rank:
                best_rank = rank
                best_index = i
        return best_index, best_rank

    def place_image_rect(self, rect_index, image_rect):
        rect = self.max_rect_list[rect_index]
        image_rect.x, image_rect.y = rect.x, rect.y

        _max_rect_list = []
        for i, rect in enumerate(self.max_rect_list):
            _max_rect_list.extend(self.cut(rect, image_rect))

        self.max_rect_list = _max_rect_list
        print("B", len(self.max_rect_list))
        self.max_rect_list = filter(self._max_rect_list_pruning, _max_rect_list)
        print("F", len(self.max_rect_list))
        self.image_rect_list.append(image_rect)

    def _max_rect_list_pruning(self, rect):
        for max_rect in self.max_rect_list:
            if rect != max_rect and rect in max_rect:
                return False

        return True


def load_images(dir_path):
    import os
    from ImageRect import ImageRect
    image_rect_list = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            file_path = os.path.join(root, f)
            _, ext = os.path.splitext(f)
            if ext == ".png":
                image_rect = ImageRect(file_path)
                image_rect_list.append(image_rect)

    return image_rect_list


def dump_max_rect(max_rect):
    from PIL import Image
    packed_image = Image.new('RGBA', max_rect.size, 0xff)

    for image_rect in max_rect.image_rect_list:
        image = image_rect.image.crop()
        if image_rect.rotated:
            image = image.transpose(Image.ROTATE_90)
        packed_image.paste(image, (image_rect.left, image_rect.top, image_rect.right, image_rect.bottom))

    return packed_image


def rect_print(rect):
    print(rect.x, rect.y, rect.width, rect.height)


def calculate_area(image_rect_list):
    area = 0
    for image_rect in image_rect_list:
        area += image_rect.area
    return


def cal_init_size(area, min_side_len=0, force_square=False):
    start_i = 0

    for i, l in enumerate(SIZE_SEQUENCE):
        if l >= min_side_len:
            start_i = i
            break

    if force_square:
        for i, l in enumerate(SIZE_SEQUENCE):
            if i < start_i:
                continue
            if area <= l*l:
                return tuple((l, l))
    else:
        for i, l in enumerate(SIZE_SEQUENCE):
            if i < start_i:
                continue
            for j in range(0, i+1):
                l2 = SIZE_SEQUENCE[j]
                if area <= l*l2:
                    return tuple((l, l2))

    raise ValueError("too larger size.")


def pack(image_rect_list):
    max_rect = MaxRects()
    max_rect_list = [max_rect]

    image_rect_list = sorted(image_rect_list, key=lambda x: max(x.width, x.height), reverse=True)

    for image_rect in image_rect_list:
        image_rect_r = image_rect.clone()
        image_rect_r.rotate()
        index, rank = max_rect.find_best_rank(image_rect)
        index_r, rank_r = max_rect.find_best_rank(image_rect_r)

        while MAX_RANK == rank_r and MAX_RANK == rank:
            max_rect.expand(MaxRects.EXPAND_SHORT_SIDE)
            index, rank = max_rect.find_best_rank(image_rect)
            index_r, rank_r = max_rect.find_best_rank(image_rect_r)

        if rank_r < rank:
            image_rect.rotate()
            index = index_r

        max_rect.place_image_rect(index, image_rect)
        # dump_max_rect(max_rect).show()

    return max_rect


def main():
    # print cal_init_size(128*128, 256, True)
    # image_rect_list = load_images("test_case/")
    # for image_rect in image_rect_list:
    #     print(image_rect.width, image_rect.height)
    #
    # max_rect = pack(image_rect_list)
    # packed_image = dump_max_rect(max_rect)
    # for rect in max_rect.max_rect_list:
    #     rect_print(rect)
    # packed_image.show()

if __name__ == '__main__':
    main()
