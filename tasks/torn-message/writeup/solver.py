from PIL import Image
import hashlib

res = Image.new('RGB', (1000, 137))

for i in range(0, 1000):
    c = str(i)
    name_object = hashlib.md5(c.encode())
    name_string = name_object.hexdigest()
    name = "{}.png".format(name_string)

    img = Image.open(name)

    res.paste(img, (i, 0))

res.save("res.png")
