===========
Quick Start
===========


Installation
============

Install Pillow with pip:

.. code:: bash

    $ pip install PyTexturePacker


Usage
=====

Here comes an example of using PyTexturePacker to pack texture images from a directory.

.. code:: python

    from PyTexturePacker import Packer

    def pack_test():
        # create a MaxRectsBinPacker
        packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00)
        # pack texture images under directory "test_case/" and name the output images as "test_case".
        # "%d" in output file name "test_case%d" is a placeholder, which is a multipack index, starting with 0.
        packer.pack("test_case/", "test_case%d")
