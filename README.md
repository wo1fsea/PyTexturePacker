# PyTexturePacker

PyTexturePacker is an open source python lib, released under the MIT License.

A subset of feature of [texturepacker](https://www.codeandweb.com/texturepacker) has been implemented in this lib. And MaxRectsBinPack algorithm which is the best-known algorithm is used in sprite sheet generation.

## License
PyTexturePacker is released under the terms of MIT License. You may find the content of the license [here](http://opensource.org/licenses/MIT), or `LICENSE.txt` inside the project directory.

## MaxRectsBinPack

    MaxRects
    * Best-known algorithm for packing textures
    * Is fast and has a high packing ratio
    * Enable rotation for best results

## Usage

Here comes an example of using PyTexturePacker to pack texture images from a directory.

    from PyTexturePacker import Packer

    def pack_test():
        # create a MaxRectsBinPacker
        packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00)
        # pack texture images under directoy "test_case/" and name the output images as "test_case".
        # "%d" in output file name "test_case%d" is a placeholder, which is a multipack index, starting with 0.
        packer.pack("test_case/", "test_case%d")

## Packer Setting

### bg_color

The background color of output image. The pixels of the empty area in the output image will be filled with bg_color.
The default value is 0x00000000, which is in format of "RGBA". A tuple of value can also be accepted, like (R, G, B, A).

### texture_format

Choose the texture format that the output file will use, for example ".jpg".
The default texture format is ".png".

### max_width

Sets the maximum width for the texture, default is 4096.

### max_height

Sets the maximum height for the texture, default is 4096.

### enable_rotated

Allows the rotating of sprites clockwise or counterclockwise by 90 degrees if they have a better fit in the texture. Might not be supported by all game/web frameworks.

### force_square

Forces the texture to have a squared size.

### shape_padding

Shape padding is the space between sprites. Value adds transparent pixels between sprites to avoid artifacts from neighbor sprites. The transparent pixels are not added to the sprites. Default is 2.
Use a value of at least 2 to avoid dragging in pixels from neighbor sprites when using OpenGL rendering.

### trim_mode

Removes transparent pixels from a sprite's border.
This shrinks the sprite's size, allows tighter packing of the sheet, and speeds up rendering since transparent pixels don't need to be processed.
Pixels with an alpha value below this value will be considered transparent when trimming the sprite.
Allowed values: 0 to 255, default is 0. When it's set to 0, the trim mode is disabled.
Very useful for sprites with nearly invisible alpha pixels at the borders.

### reduce_border_artifacts

Adds color to transparent pixels by repeating a sprite's outer color values.
These color values can reduce artifacts around sprites and removes dark halos at transparent borders. This feature is also known as "Alpha bleeding".

## Contributing
Any types of contribution are welcome. Thanks.

