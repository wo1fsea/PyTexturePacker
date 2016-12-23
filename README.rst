PyTexturePacker |build-status| |docs-status|
============================================

PyTexturePacker is an open source python package, released under the MIT License.

A subset of feature of TexturePacker_ has been implemented in this package.

.. _TexturePacker: https://www.codeandweb.com/texturepacker

Features
========

MaxRectsBinPack algorithm is used to generate sprite sheet in this package.

MaxRectsBinPack
---------------

MaxRectsBinPack is currently the best packing algorithm.
It tries to use the least texture space by applying different heuristics when placing the sprites.

- MaxRects

    - Best-known algorithm for packing textures
    - Is fast and has a high packing ratio
    - Enable rotation for best results


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


Packer Setting
==============

bg_color
--------

The background color of output image. The pixels of the empty area in the output image will be filled with bg_color.
The default value is 0x00000000, which is in format of "RGBA". A tuple of values can also be accepted, like (R, G, B, A).

texture_format
--------------

Choose the texture format that the output file will use, for example ".jpg".
The default texture format is ".png".

max_width
---------

Sets the maximum width for the texture, default is 4096.

max_height
----------

Sets the maximum height for the texture, default is 4096.

enable_rotated
--------------

Allows the rotating of sprites clockwise or counterclockwise by 90 degrees if they have a better fit in the texture. Might not be supported by all game/web frameworks.

force_square
------------

Forces the texture to have a squared size.

border_padding
--------------

Border padding is the space between the sprites and the border of the sprite sheet. Value adds transparent pixels around the borders of the sprite sheet. Default is 2.

shape_padding
-------------

Shape padding is the space between sprites. Value adds transparent pixels between sprites to avoid artifacts from neighbor sprites. The transparent pixels are not added to the sprites. Default is 2.
Use a value of at least 2 to avoid dragging in pixels from neighbor sprites when using OpenGL rendering.

inner_padding
-------------

Adds transparent pixels to the inside of the sprite, growing it. Default is 0.

There are two uses for this:

- It can help in preventing cut-off artifacts near the edges of scaled sprites. E.g. if your sprite has a few pixels along its own boundaries, scaling the sprite up or down won't let these pixels appear as gaps or cuts.
- It considerably reduces aliasing along the polygon edges when rotating trimmed or cropped sprites. E.g. if your sprite has many pixels along its own boundaries, it will be drawn more smoothly when rotating it.

trim_mode
---------

Removes transparent pixels from a sprite's border.
This shrinks the sprite's size, allows tighter packing of the sheet, and speeds up rendering since transparent pixels don't need to be processed.
Pixels with an alpha value below this value will be considered transparent when trimming the sprite.
Allowed values: 0 to 255, default is 0. When it's set to 0, the trim mode is disabled.
Very useful for sprites with nearly invisible alpha pixels at the borders.

reduce_border_artifacts
-----------------------

Adds color to transparent pixels by repeating a sprite's outer color values.
These color values can reduce artifacts around sprites and removes dark halos at transparent borders. This feature is also known as "Alpha bleeding".


Contribute
==========

- Issue Tracker: github.com/wo1fsea/PyTexturePacker/issues
- Source Code: github.com/wo1fsea/PyTexturePacker

Any types of contribution are welcome. Thanks.


Support
=======

If you are having issues, please let us know.
Please feel free to contact me. email: quanyongh@foxmail.com


License
=======

The project is released under the terms of MIT License. You may find the content of the license here_, or `LICENSE.txt` inside the project directory.

.. _here: http://opensource.org/licenses/MIT



.. |build-status| image:: https://travis-ci.org/wo1fsea/PyTexturePacker.svg?branch=master
    :target: https://travis-ci.org/wo1fsea/PyTexturePacker
    :alt: Build status
.. |docs-status| image:: https://readthedocs.org/projects/pytexturepacker/badge/?version=master
    :target: http://pytexturepacker.readthedocs.io/
    :alt: Documentation Status
   
