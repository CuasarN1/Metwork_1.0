from math import sqrt
from PIL import Image
from random import choice

path = "yes/2020_02_17_11_59_22.png"


def zero(h, per):
    for v in h.values():
        if v < per:
            return True
    return False


def pick(h, per):
    while True:
        key = choice(list(h.keys()))
        if h[key] < per:
            return key


def pack(h, per):
    while zero(h, per):
        key = pick(h, per)
        val = h[key]
        col = similar(h, key)
        if h[col] > val:
            h[col] += h.pop(key)
        else:
            h[key] += h.pop(col)


def similar(h, col):
    min_dist = 442
    closest = (-1, -1, -1)
    for k in h.keys():
        if k != col:
            dist = sqrt(pow(k[0] - col[0], 2) +
                        pow(k[1] - col[1], 2) +
                        pow(k[2] - col[2], 2))
            if dist < min_dist:
                min_dist = dist
                closest = k
    return closest


try:
    img = Image.open(path, 'r')

except FileNotFoundError:
    print("Файл не найден")

mode = img.mode
size = img.size
x, y = size[0], size[1]
total = x * y * 1.0
percent = round(total / 100)
# print(x, y)

ColorTable = {}
for i in range(x):
    for j in range(y):
        # print(i, j)
        clr = img.getpixel((i, j))
        # if len(clr) == 4:
        #    clr = (clr[0], clr[1], clr[2])
        if ColorTable.get(clr) is None:
            ColorTable[clr] = 1
        else:
            ColorTable[clr] += 1

pack(ColorTable, percent)
sortCLR = sorted(ColorTable.items(), reverse=True, key=lambda kv: kv[1])
print(total, len(sortCLR), sortCLR)

p = 100.00
ans = {}
for e in sortCLR:
    curr = e[1] / total * 100
    if mode == "RGBA":
        col = (e[0][0], e[0][1], e[0][2])
    else:
        col = e[0]
    ans[col] = str(round(curr, 3)) + " %"
    p -= curr

if p >= 0.001:
    ans["other"] = str(p) + " %"

for e in ans.items():
    print(e)
