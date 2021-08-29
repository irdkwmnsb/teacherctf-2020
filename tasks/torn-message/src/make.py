from PIL import Image
from hashlib import md5
import os
import tqdm

DIR = "files"

os.makedirs(DIR, True)
im = Image.open("orig.png")  # type: Image.Image
print(im.width)
print(im.height)
for i in tqdm.tqdm(range(im.width)):
    new = im.crop((i, 0, i + 1, im.height))
    new.save(DIR + "/" + md5(str(i).encode()).hexdigest() + ".png")
