from math import sqrt
from PIL import Image
import os
from contextlib import redirect_stdout
import tensorflow as tf
from random import choice
eps = 15
min_col = 50
max_col = 650
borders = range(min_col, max_col)

def test(arr, total, mode):
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
    return ans


def distance(img):
    img = img.convert('P', palette=Image.ADAPTIVE, colors=eps).convert("RGB")
    colors = Image.Image.getcolors(img)
    # mode = img.mode
    # size = img.size
    # total = size[0] * size[1] * 1.0

    # sortCLR = sorted(colors, reverse=True, key=lambda kv: kv[0])
    # trim = list(filter(lambda c: c[1][0] + c[1][1] + c[1][2] in borders, sortCLR))
    # d = diff(trim)

    # print(len(trim), trim)
    # print(len(sortCLR), sortCLR)
    # test(sortCLR, total, mode)
    # print(len(d), d)

    return sorted(diff(colors))


folds = ['yes', 'no']
for d in folds:
    num = 0
    path_arr = []
    for path in os.listdir(d):
        full_path = os.path.join(d, path)
        if os.path.isfile(full_path):
            path_arr.append(full_path)
            num += 1

    most = []
    # for path in path_arr:
    #    img = Image.open(path, 'r')
    #    most.append(distance(img))

    # print(sum(most) * 1.0 / len(most))

    # hello = tf.constant('Hello, TensorFlow')
    # sess = tf.compat.v1.Session()
    # print(sess.run(hello))

    file = []
    max_min = -9999999999.0
    max_max = -9999999999.0
    max_avg = -9999999999.0
    cnt1, cnt2 = 0, 0

    for path in path_arr:
        img = Image.open(path, 'r')
        orig = distance(img)
        most = []
        file.append(path)
        file.append('')
        # for s in range(120, 180, 5):
        r, g, b = img.split()
        j = 1.45
        r = r.point(lambda i: i * j)
        g = g.point(lambda i: i * j)
        b = b.point(lambda i: i * j)
        result = Image.merge('RGB', (r, g, b))
        new = distance(result)

        omin, omax, oavg = min(orig), max(orig), sum(orig) / len(orig)
        nmin, nmax, navg = min(new), max(new), sum(new) / len(new)
        labs, rabs, aabs = abs(omin - nmin), abs(omax - nmax), abs(oavg - navg)
        max_min, max_max, max_avg = max(max_min, labs), max(max_max, rabs), max(max_avg, aabs)
        if labs >= 7.5: cnt1 += 1
        if labs >= 9.0: cnt2 += 1

        file.append('rgb shift: ' + str(j))
        file.append('orig min, max, mid: ' + str(omin) + ' ; ' + str(omax) + ' ; ' + str(oavg))
        file.append('new min, max, mid: ' + str(nmin) + ' ; ' + str(nmax) + ' ; ' + str(navg))
        file.append('abs min max, mid: ' + str(labs) + ' ; ' + str(rabs) + ' ; ' + str(aabs))
        file.append(120 * '-')

    with open(d + '.txt', 'w') as f:
        with redirect_stdout(f):
            for line in file:
                print(line)

    print(d)
    print(max_min, max_max, max_avg)
    print(cnt2, cnt1)
    print(num, '\n')
