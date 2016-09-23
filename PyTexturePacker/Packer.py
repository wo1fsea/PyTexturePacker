import random
import math


def cut_rect(main_rect, sub_rect):
    main_l, main_t, main_r, main_b = main_rect
    sub_l, sub_t, sub_r, sub_b = sub_rect

    if main_b < sub_t or main_l > sub_r or main_r < sub_l or main_t > sub_b:
        return [main_rect, ]

    sub_l = main_l if sub_l < main_l else sub_l
    sub_t = main_t if sub_t < main_t else sub_t
    sub_r = main_r if sub_r > main_r else sub_r
    sub_b = main_b if sub_b > main_b else sub_b

    l = (main_t, main_l, main_b, sub_l) if main_l < sub_l else None
    t = (main_t, main_l, sub_t, main_r) if main_t < sub_t else None
    r = (main_t, sub_r, main_b, main_r) if main_r > sub_r else None
    b = (sub_b, main_l, main_b, main_r) if main_b > sub_b else None

    return filter(lambda x: x, (l, t, r, b))


def is_in_rect(main_rect, sub_rect):
    main_l, main_t, main_r, main_b = main_rect
    sub_l, sub_t, sub_r, sub_b = sub_rect

    return main_l <= sub_l and main_t <= sub_t and main_r >= sub_r and main_b >= sub_b


def rank():
    pass


def expand(max_rects, cur):
    pass


def select_best(max_rect_list, img):
    img_w, img_h = img
    for i, max_rect in enumerate(max_rect_list):
        w, h = max_rect[2] - max_rect[0], max_rect[3] - max_rect[1]
        print(w, h, img_w, img_h)
        if w >= img_w and h >= img_h:
            return i
    return -1


def max_rects_bin_Pack(max_rect, imgs):
    max_rect_list = [max_rect]
    _imgs = []

    for img in imgs:
        print(max_rect_list)
        index = select_best(max_rect_list, img)

        if index == -1:
            print("Can't not fit.")
            return

        x, y = max_rect_list[index][:2]
        w, h = img
        img_rect = (x, y, x + w, y + h)
        _imgs.append(img_rect)

        _max_rect_list = []
        for max_rect in max_rect_list:
            _max_rect_list.extend(cut_rect(max_rect, img_rect))

        max_rect_list = _max_rect_list

    return max_rect_list, _imgs


def gen_rect_data():
    return [random.randint(0, 100), random.randint(0, 100)]


def main():
    a = (0, 0, 100, 100)
    b = ((50, 100), (10, 100)) #(20, 20), )
    print(max_rects_bin_Pack(a, b)[1])


if __name__ == '__main__':
    main()
