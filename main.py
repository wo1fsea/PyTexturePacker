# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
    Huang Quanyong (wo1fSea)
    quanyongh@foxmail.com
Date:
    2016/10/19
Description:
    main.py
----------------------------------------------------------------------------"""

from PyTexturePacker import Packer
from PyTexturePacker import Project


def pack_test():
    # create a MaxRectsPacker
    packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00, atlas_format="csv")
    # pack texture images under the directory "test_case/" and name the output images as "test_case".
    # "%d" in output file name "test_case%d" is a placeholder, which is the atlas index, starting with 0.
    packer.pack("test_image/", "test_image%d", "")


def project_test():
    packer_args = Project.PackerArgs(max_width=2048, max_height=2048, bg_color=0xffffffff, atlas_format="csv")
    project = Project.Project()
    project.set_project_name("test_project")
    project.set_packer_args(packer_args)
    project.packs_data.append(Project.PackData(input_images="test_image/", output_name="test_image%d", output_path=""))
    project.save("test_project.json")
    project.load("test_project.json")
    project.pack()


def main():
    pack_test()
    project_test()


if __name__ == '__main__':
    main()
