=======
Options
=======

Packer Setting
==============

This chapter describes the options used to create a MaxRectsBinPacker.

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

