# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2024/03/02
Description:
    Project.py
----------------------------------------------------------------------------"""

from . import Utils
from . import Packer


def get_packer_types():
    """
    get all packer types
    :return: a list of packer types
    """
    return [Packer.MaxRectsPacker, Packer.GuillotinePacker]


def get_packer_type_names():
    """
    get all packer type names
    :return: a list of packer type names
    """
    return [packer_type.__name__ for packer_type in get_packer_types()]


def get_packer_type_by_name(packer_name):
    """
    get a packer type by name
    :param packer_name: the name of the packer
    :return: the type
    """
    for packer_type in get_packer_types():
        if packer_type.__name__ == packer_name:
            return packer_type
    return Packer.MaxRectsPacker  # default packer


def load_project(file_path):
    """
    load a project from file
    :param file_path: the file path to load
    :return: the loaded project
    """
    project = Project()
    project.load(file_path)
    return project


class PackData(object):
    def __init__(self, input_images=None, output_name="output%d", output_path="", input_base_path=None):
        self.input_images = input_images if input_images else []
        self.output_name = output_name
        self.output_path = output_path
        self.input_base_path = input_base_path

    def get_pack_params(self):
        return {
            "input_images": self.input_images,
            "output_name": self.output_name,
            "output_path": self.output_path,
            "input_base_path": self.input_base_path,
        }

    def add_image(self, image):
        self.input_images.append(image)

    def remove_image(self, image):
        self.input_images.remove(image)

    def clear_images(self):
        self.input_images.clear()


class PackerArgs(object):
    def __init__(self, bg_color=0x00000000, texture_format=".png", max_width=4096, max_height=4096, enable_rotated=True,
                 force_square=False, border_padding=2, shape_padding=2, inner_padding=0, trim_mode=0,
                 reduce_border_artifacts=False, extrude=0, atlas_format=Utils.ATLAS_FORMAT_PLIST, atlas_ext=None):
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
        self.extrude = extrude
        self.atlas_format = atlas_format
        self.atlas_ext = atlas_ext

    def get_pack_params(self):
        return {
            "bg_color": self.bg_color,
            "texture_format": self.texture_format,
            "max_width": self.max_width,
            "max_height": self.max_height,
            "enable_rotated": self.enable_rotated,
            "force_square": self.force_square,
            "border_padding": self.border_padding,
            "shape_padding": self.shape_padding,
            "inner_padding": self.inner_padding,
            "trim_mode": self.trim_mode,
            "reduce_border_artifacts": self.reduce_border_artifacts,
            "extrude": self.extrude,
            "atlas_format": self.atlas_format,
            "atlas_ext": self.atlas_ext,
        }


class Project(object):
    def __init__(self):
        self._project_name = "unknown_project"
        self._packer_type_name = None
        self._packer_args = PackerArgs()
        self._packs = []  # PackData list
        self._packer = None

        self.refresh_packer()

    def _create_packer(self, packer_type_name, *args, **kwargs):
        """
        create a texture packer
        :param packer_type_name: the type name of packer to create
        :param args:
        :param kwargs:
        :return:
        """
        packer_type = get_packer_type_by_name(packer_type_name)
        self._packer = Packer.create(packer_type, *args, **kwargs)
        return self._packer

    @property
    def project_name(self):
        return self._project_name

    def set_project_name(self, name):
        self._project_name = name

    def set_packer_args(self, packer_args):
        self._packer_args = packer_args
        self.refresh_packer()

    @property
    def packer_type_name(self):
        return self._packer_type_name

    def set_packer_type_name(self, packer_type_name):
        self._packer_type_name = packer_type_name
        self.refresh_packer()

    @property
    def packs_data(self):
        return self._packs

    def load(self, file_path):
        """
        load a project from file
        :param file_path: the file path to load
        :return:
        """

        # load the project info from json
        import json
        with open(file_path, 'r') as fp:
            project_info = json.load(fp)

        self._project_name = project_info["project_name"]
        self._packer_type_name = project_info["packer_type_name"]
        self._packer_args = PackerArgs(**project_info["packer_args"])
        self._packs = []

        for pack_data in project_info["packs"]:
            self._packs.append(PackData(**pack_data))

    def save(self, file_path):
        """
        save the project to file
        :param file_path: the file path to save
        :return:
        """

        # save the project info to json
        import json
        project_info = {
            "project_name": self._project_name,
            "packer_type_name": self._packer_type_name,
            "packer_args": self._packer_args.get_pack_params(),
            "packs": [pack.get_pack_params() for pack in self._packs]
        }

        with open(file_path, 'w') as fp:
            json.dump(project_info, fp, indent=4, sort_keys=True)

    def refresh_packer(self):
        """
        refresh the packer
        :return:
        """
        self._create_packer(self._packer_type_name, **self._packer_args.get_pack_params())

    def pack(self, multi_process=False):
        """
        pack the project
        :return:
        """
        if multi_process:
            self._packer.multi_pack(self._packs)
        else:
            for pack in self._packs:
                self._packer.pack(**pack.get_pack_params())
