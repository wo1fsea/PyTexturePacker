
SUPPORTED_IMAGE_FORMAT = [".png", ".jpg", ".bmp"]


def load_images_from_paths(image_path_list):
    from .ImageRect import ImageRect

    image_rect_list = []
    for file_path in image_path_list:
        image_rect = ImageRect(file_path)
        image_rect_list.append(image_rect)

    return image_rect_list


def load_images_from_dir(dir_path):
    import os

    image_rect_path = []
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            file_path = os.path.join(root, f)
            _, ext = os.path.splitext(f)
            if ext.lower() in SUPPORTED_IMAGE_FORMAT:
                image_rect_path.append(file_path)

    return load_images_from_paths(image_rect_path)


def save_plist(data_dict, file_name):
    import plistlib

    with open(file_name, 'wb') as fp:
        plistlib.dump(data_dict, fp)


def save_image(image, file_name):
    image.save(file_name)
