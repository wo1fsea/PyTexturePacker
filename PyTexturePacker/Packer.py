from .MaxRectsBinPacker.MaxRectsBinPacker import MaxRectsBinPacker

TYPE_MAX_RECTS_BIN_PACK = MaxRectsBinPacker

def create(packer_type=TYPE_MAX_RECTS_BIN_PACK, *args, **kwargs):
	return MaxRectsBinPacker(*args, **kwargs)

