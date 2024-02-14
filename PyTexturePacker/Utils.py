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

import sys
import inspect
if sys.version_info.major > 2:
    xrange = range

SUPPORTED_IMAGE_FORMAT = [".png", ".jpg", ".bmp"]
ATLAS_FORMAT_PLIST = "plist"
ATLAS_FORMAT_JSON = "json"
ATLAS_FORMAT_CSV = "csv"


def load_images_from_paths(image_path_list):
    """
    load image form paths
    :param image_path_list: image paths list
    :return: ImageRect list
    """
    from .ImageRect import ImageRect

    image_rect_list = []
    for file_path in image_path_list:
        image_rect = ImageRect(file_path)
        image_rect_list.append(image_rect)

    return image_rect_list


def load_images_from_dir(dir_path):
    """
    load all images from a directory
    :param dir_path: directory path
    :return: ImageRect list
    """
    import os

    image_rect_path = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            file_path = os.path.join(root, f)
            _, ext = os.path.splitext(f)
            if ext.lower() in SUPPORTED_IMAGE_FORMAT:
                image_rect_path.append(file_path)

    return load_images_from_paths(image_rect_path)


def get_atlas_data_ext(atlas_format):
    """
    get default file extension for selected type of atlas data file
    :param atlas_format: atlas data file format
    :return:
    """
    if atlas_format == ATLAS_FORMAT_PLIST:
        return '.plist'
    elif atlas_format == ATLAS_FORMAT_JSON:
        return '.json'
    elif atlas_format == ATLAS_FORMAT_CSV:
        return '.csv'
    elif callable(atlas_format):
        parameters = inspect.signature(atlas_format).parameters
        required_args = sum(1 for param in parameters.values()
                            if param.default is param.empty)
        if len(parameters) >= 2 and required_args <= 2:
            return '.txt'

    raise ValueError("Unsupported file format: %s" % atlas_format)


def save_atlas_data(data_dict, file_path, atlas_format):
    """
    save a atlas data in selected format. plist or json supported
    :param data_dict: dict data
    :param file_path: file path to save
    :param atlas_format: atlas data file format
    :return:
    """
    if atlas_format == ATLAS_FORMAT_PLIST:
        return save_plist(data_dict, file_path)
    elif atlas_format == ATLAS_FORMAT_JSON:
        return save_json(data_dict, file_path)
    elif atlas_format == ATLAS_FORMAT_CSV:
        return save_csv(data_dict, file_path)
    elif callable(atlas_format):
        parameters = inspect.signature(atlas_format).parameters
        required_args = sum(1 for param in parameters.values()
                            if param.default is param.empty)
        if len(parameters) >= 2 and required_args <= 2:
            return atlas_format(data_dict, file_path)

    raise ValueError("Unsupported file format: %s" % atlas_format)


def save_csv(data_dict, file_path):
    """
    save a dict as a csv
    :param data_dict: dict data
    :param file_path: csv file path to save
    :return:
    """
    with open(file_path, 'w') as fp:
        for name, data in data_dict['frames'].items():
            frame = data['frame']
            source = data['spriteSourceSize']

            # fp.write(f'{name},{frame["x"]},{frame["y"]},{frame["w"]},{frame["h"]},'
            #          f'{source["x"]},{source["y"]},{source["w"]},{source["h"]},'
            #          f'{data["rotated"]},{data["trimed"]}\n')
            fp.write('%s,%d,%d,%d,%d,%d,%d,%d,%d,%s,%s\n' % (name, frame["x"], frame["y"], frame["w"], frame["h"],
                                                             source["x"], source["y"], source["w"], source["h"],
                                                             data["rotated"], data["trimed"]))


def save_json(data_dict, file_path):
    """
    save a dict as a json file
    :param data_dict: dict data
    :param file_path: json file path to save
    :return:
    """
    import json
    with open(file_path, 'w') as fp:
        json.dump(data_dict, fp)


def save_plist(data_dict, file_path):
    """
    save a dict as a plist file
    :param data_dict: dict data
    :param file_path: plist file path to save
    :return:
    """
    import plistlib

    if hasattr(plistlib, "dump"):
        with open(file_path, 'wb') as fp:
            plistlib.dump(data_dict, fp)
    else:
        plistlib.writePlist(data_dict, file_path)


def save_image(image, file_path):
    """
    save a Image as a file
    :param image: Image
    :param file_path: file path to save
    :return:
    """
    image.save(file_path)


def alpha_bleeding(image, bleeding_pixel=8):
    """
    alpha bleeding
    :param image: Image
    :param bleeding_pixel: pixel to bleed
    :return:
    """
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
            if 0 <= ox < width and 0 <= oy < height and pa[ox, oy][3] == 0:
                return True
        return False

    def _bleeding(x, y):
        borders = []
        pixel = pa[x, y]
        for offset in offsets:
            ox = x + offset[0]
            oy = y + offset[1]
            if 0 <= ox < width and 0 <= oy < height and pa[ox, oy][3] == 0 and (ox, oy) not in bleeding:
                pa[ox, oy] = (pixel[0], pixel[1], pixel[2], 1)
                bleeding.add((ox, oy))
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
    """
    remove the alpha channel of the image(set as 255)
    :param image: Image
    :return:
    """
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


def clean_pixel_alpha_below(image, v=1):
    """
    clean pixels of the image which alpha channel is below the given value
    :param image: Image
    :param v: given value
    :return:
    """
    image = image.copy()
    width, height = image.size
    if image.mode != "RGBA":
        image = image.convert("RGBA")

    pa = image.load()
    for x in range(width):
        for y in range(height):
            pixel = pa[x, y]
            if pixel[3] < v:
                pa[x, y] = (0, 0, 0, 0)
    return image


def _border(border):
    if isinstance(border, tuple):
        if len(border) == 2:
            left, top = right, bottom = border
        elif len(border) == 4:
            left, top, right, bottom = border
    else:
        left = top = right = bottom = border
    return left, top, right, bottom


def extrude_image(image, border=0):
    if border == 0:
        return image

    from PIL import Image
    left, top, right, bottom = _border(border)
    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    out = Image.new(image.mode, (width, height))
    out.paste(image, (left, top))
    for x in xrange(width):
        if 0 <= x < left:
            ref_x = left
        elif x >= left + image.size[0]:
            ref_x = left + image.size[0] - 1
        else:
            ref_x = x
        p = out.getpixel((ref_x, top))
        for y in xrange(top):
            out.putpixel((x, y), p)

    for y in xrange(top, top + image.size[1]):
        p = out.getpixel((left, y))
        for x in xrange(left):
            out.putpixel((x, y), p)

    for y in xrange(top, top + image.size[1]):
        p = out.getpixel((left + image.size[0] - 1, y))
        for x in xrange(left + image.size[0], width):
            out.putpixel((x, y), p)

    for x in xrange(width):
        if 0 <= x < left:
            ref_x = left
        elif x >= left + image.size[0]:
            ref_x = left + image.size[0] - 1
        else:
            ref_x = x
        p = out.getpixel((ref_x, top + image.size[1] - 1))
        for y in xrange(top + image.size[1], height):
            out.putpixel((x, y), p)
    return out
