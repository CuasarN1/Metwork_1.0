from math import sqrt
from PIL import Image
from random import choice

path = "no/2020_02_17_11_53_37.png"
eps = 20
min_col = 80
max_col = 600


try:
    img = Image.open(path, 'r')

except FileNotFoundError:
    print("Файл не найден")

img = img.convert('P', palette=Image.ADAPTIVE, colors = eps).convert("RGB")
colors = Image.Image.getcolors(img)
img.show()
mode = img.mode
size = img.size
x = size[0]
y = size[1]
total = x * y * 1.0
percent = round(total / 100)
# print(x, y)

sortCLR = sorted(colors, reverse=True, key=lambda kv: kv[0])
print(total, len(sortCLR), sortCLR)

p = 100.00
ans = {}
for e in sortCLR:
    curr = e[0] / total * 100
    if mode == "RGBA":
        col = (e[1][0], e[1][1], e[1][2])
    else:
        col = e[1]
    ans[col] = str(round(curr, 3)) + " %"
    p -= curr

if p >= 0.001:
    ans["other"] = str(p) + " %"

for e in ans.items():
    print(e)
