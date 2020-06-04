"""
pillow でmatplotlib 保存画像を切り取り
"""

from PIL import Image
import image_to_text


def crop_by_pil(select_lang, start_x, start_y, current_X, current_y, path,
                resize_height, resize_width, dir_path):
    """
    pillowでトリミング
    """
    im = Image.open(path)
    width = im.width
    height = im.height
    cx0 = round(width * start_x /resize_width)
    cy0 = round(height * start_y / resize_height)
    cx1 = round(width * current_X / resize_width)
    cy1 = round(height * current_y / resize_height)

    im_crop = im.crop((cx0, cy0, cx1, cy1))
    im_crop.save("cropped.png")

    image_path_list = []
    image_path_list.append("cropped.png")
    itt = image_to_text.Image_to_Text()
    itt.image_to_text(image_path_list=image_path_list, select_lang=select_lang, dir_path=dir_path)