import shutil
import os
from PIL import Image
import tqdm

shutil.rmtree("frames", ignore_errors=True)
os.mkdir("frames")
with open("log.txt", "r") as f:
    lines = f.readlines()[1:]

img = Image.new("1", (37, 37), "white")
for frame_n, line in tqdm.tqdm(enumerate(lines)):
    x, y, col = map(int, line.split(','))
    img.putpixel((x + 2, y + 2), col)
    file_name = "frames/%04d.bmp" % frame_n
    img.resize(((37 * 4), (37 * 4))).save(file_name)

os.system(
    'ffmpeg.exe -f image2 -framerate 25 -pattern_type sequence -start_number 0 -r 60 -i "frames/%04d.bmp" -s 116x116 test.avi')
shutil.rmtree("frames", ignore_errors=True)
