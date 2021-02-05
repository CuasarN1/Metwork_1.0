from math import sqrt
from PIL import Image
import os
# import tensorflow as tf
from random import choice


def test(arr):
    p = 100.00
    ans = {}
    for e in arr:
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


def diff(arr):
    ans = []
    n = len(arr)
    for i in range(n - 1):
        for j in range(i + 1, n):
            f, s = arr[i][1], arr[j][1]
            ans.append(sqrt(pow(f[0] - s[0], 2) + pow(f[1] - s[1], 2) + pow(f[2] - s[2], 2)))
    return sorted(ans, reverse=True)


d = "no"
path_arr = []
for path in os.listdir(d):
    full_path = os.path.join(d, path)
    if os.path.isfile(full_path):
        path_arr.append(full_path)

# path = "no/2020_02_17_11_53_37.png"
eps = 15
min_col = 50
max_col = 650
r = range(min_col, max_col)

most = []

for path in path_arr:

    try:
        img = Image.open(path, 'r')

    except FileNotFoundError:
        print("Файл не найден")

    img = img.convert('P', palette=Image.ADAPTIVE, colors=eps).convert("RGB")
    colors = Image.Image.getcolors(img)
    # img.show()
    mode = img.mode
    size = img.size
    x, y = size[0], size[1]
    total = x * y * 1.0
    percent = round(total / 100)
    # print(x, y)

    sortCLR = sorted(colors, reverse=True, key=lambda kv: kv[0])

    trim = [c for c in sortCLR if c[1][0] + c[1][1] + c[1][2] in r]

    # print(len(trim), trim)
    # print(len(sortCLR), sortCLR)
    # test(sortCLR)
    d = diff(trim)
    # print(len(d), d)

    most.append(d[0])

print(sum(most) * 1.0 / len(most))