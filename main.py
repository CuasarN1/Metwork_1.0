from math import sqrt
from PIL import Image
from random import choice

path = "no/2020_02_17_11_53_37.png"
eps = 15
min_col = 80
max_col = 600


try:
    img = Image.open(path, 'r')

except FileNotFoundError:
    print("Файл не найден")

img = img.convert('P', palette=Image.ADAPTIVE, colors = eps).convert("RGB")
img.show()
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
