import base64
import random

def decode(s, key):
    alphs = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz", "0123456789"]
    new_s = []
    for i in s:
        for alph in alphs:
            if i in alph:
                new_s.append(alph[(alph.index(i) - key) % len(alph)])
                break
        else:
            new_s.append(i)
    return base64.b64decode(''.join(new_s).encode())


if __name__ == "__main__":
    enc = input()
    for key in range(0, 26*10//2):
        s = decode(enc, key)
        if s.startswith(b'TeacherCTF'):
            print(s.decode())