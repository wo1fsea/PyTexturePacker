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

    from PyTexturePacker import Packer

    def pack_test():
        packer = Packer.create(max_width=2048, max_height=2048, bg_color=0xffffff00)
        packer.pack("test_case/", "test_case%d")


## Contributing
Any types of contribution are welcome. Thanks.

