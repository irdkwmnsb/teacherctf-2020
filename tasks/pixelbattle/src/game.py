import qrcode
import numpy as np
from players import ImagePlayer, ChaoticPlayer
from PIL import Image

img = qrcode.make("SICAMP{pix3l_battl3_but_1ts_cha0tic_hsugehf}", box_size=1, border=0)
dest_img = np.array(img)
cnv = np.zeros(img.size, dtype=np.bool)+1

actions = []
phases = [
    (15, 70, 30),  # 100 mins [70 chaotic, 30 good]
    (20, 5, 90),  # 80 mins [10 chaotic, 90 good] ## 85*10 = 800/
    (18, 90, 10)  # 120 mins [90 chaotic, 10 good]
]
if __name__ == "__main__":
    for phase in phases:
        players = [ChaoticPlayer(img.size) for _ in range(phase[1])] + \
                  [ImagePlayer(img.size, dest_img) for _ in range(phase[2])]
        for i in range(phase[0]):
            for player in players:
                move = player.place(cnv)
                if move is None:
                    continue
                x, y, col = move
                cnv[x][y] = col
                actions.append((x, y, int(col)))

print(len(actions))
with open("../files/log.txt", "w") as f:
    print("x,y,col", file=f)
    for action in actions:
        print(*action, sep=',', file=f)
