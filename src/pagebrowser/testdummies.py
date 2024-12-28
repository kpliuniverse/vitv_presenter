import random, os
import PIL.Image, PIL.ImageFile

DUMMY_PATH = "./dummies/images"
def random_dummy_image(size=None):

    x = random.choice(os.listdir(DUMMY_PATH))


    with open(f"{DUMMY_PATH}/{x}", "rb") as f:
        x_f = PIL.ImageFile.Parser()
        x_f.feed(f.read())
        x = x_f.close()
        if size:
            return x.resize(size, PIL.Image.Resampling.LANCZOS)
        return x