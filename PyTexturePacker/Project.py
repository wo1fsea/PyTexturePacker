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


def load_project(file_path):
    """
    load a project from file
    :param file_path: the file path to load
    :return: the loaded project
    """
    project = Project()
    project.load(file_path)
    return project


class Project(object):
    def __init__(self):
        self._project_name = "unknown_project"
        self._packer = None
        self._packer_type = None
        self._packer_args = {}
        self._packs = []  # {input_images, output_name, output_path="", input_base_path=None}

    def _create_packer(self, packer_type, *args, **kwargs):
        """
        create a texture packer
        :param packer_type: the type of packer to create
        :param args:
        :param kwargs:
        :return:
        """
        self._packer = packer_type(*args, **kwargs)
        self._packer_type = packer_type
        return self._packer

    @property
    def packer_type(self):
        return self._packer_type

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
        self._packer_type = project_info["packer_type"]
        self._packer_args = project_info["packer_args"]
        self._packs = project_info["packs"]

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
            "packer_type": self._packer_type.__name__,
            "packer_args": self._packer_args,
            "packs": self._packs,
        }

        with open(file_path, 'w') as fp:
            json.dump(project_info, fp)

    def pack(self, multi_process=False):
        """
        pack the project
        :return:
        """
        if multi_process:
            self._packer.multi_pack(self._packs)
        else:
            for pack in self._packs:
                self._packer.pack(**pack)


