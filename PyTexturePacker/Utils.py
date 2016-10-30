# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    Utils.py
----------------------------------------------------------------------------"""

SUPPORTED_IMAGE_FORMAT = [".png", ".jpg", ".bmp"]


def load_images_from_paths(image_path_list):
    from .ImageRect import ImageRect

    image_rect_list = []
    for file_path in image_path_list:
        image_rect = ImageRect(file_path)
        image_rect_list.append(image_rect)

    return image_rect_list


def load_images_from_dir(dir_path):
    import os

    image_rect_path = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            file_path = os.path.join(root, f)
            _, ext = os.path.splitext(f)
            if ext.lower() in SUPPORTED_IMAGE_FORMAT:
                image_rect_path.append(file_path)

    return load_images_from_paths(image_rect_path)


def save_plist(data_dict, file_name):
    import plistlib

    if hasattr(plistlib, "dump"):
        with open(file_name, 'wb') as fp:
            plistlib.dump(data_dict, fp)
    else:
        plistlib.writePlist(data_dict, file_name)


def save_image(image, file_name):
    image.save(file_name)


def alpha_bleeding(image, bleeding_pixel=32):
    offsets = ((-1, -1), (0, -1), (1, -1),
               (-1, 0), (1, 0),
               (-1, 1), (0, 1), (1, 1))

    image = image.copy()
    width, height = image.size
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    pa = image.load()

    bleeding = set()
    borders = []

    def _tell_border(x, y):
        if pa[x, y][3] == 0:
            return False

        for offset in offsets:
            ox = x + offset[0]
            oy = y + offset[1]
            if ox >= 0 and ox < width and oy >= 0 and oy < height \
                    and pa[ox, oy][3] == 0:
                return True
        return False

    def _bleeding(x, y):
        borders = []
        pixel = pa[x, y]
        for offset in offsets:
            ox = x + offset[0]
            oy = y + offset[1]
            if ox >= 0 and ox < width and oy >= 0 and oy < height \
                    and pa[ox, oy][3] == 0 and (ox, oy) not in bleeding:
                pa[ox, oy] = (pixel[0], pixel[1], pixel[2], 0)
                bleeding.add(pa)
                if _tell_border(ox, oy):
                    borders.append((ox, oy))
        return borders

    for x in range(width):
        for y in range(height):
            if _tell_border(x, y):
                borders.append((x, y))

    for i in range(bleeding_pixel):
        pending = []
        for border in borders:
            pending.extend(_bleeding(*border))
        borders = pending

    return image


def alpha_remove(image):
    image = image.copy()
    width, height = image.size
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    pa = image.load()
    for x in range(width):
        for y in range(height):
            pixel = pa[x, y]
            pa[x, y] = (pixel[0], pixel[1], pixel[2], 255)
    return image
