from MaxRectsBinPacker.MaxRectsBinPacker import MaxRectsBinPacker


def main():
    packer = MaxRectsBinPacker(max_width=256)
    packer.pack("test_case/", "test_case")


if __name__ == '__main__':
    main()
