

import PIL.Image


def blank_img(w: int, h: int):
    # Create a new blank image
    img = PIL.Image.new('RGB', (w, h), color=(0, 0, 0))
    return img