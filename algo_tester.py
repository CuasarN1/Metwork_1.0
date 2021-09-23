from math import sqrt
from imageai.Classification.Custom import CustomImageClassification
from PIL import Image
import glob


def distance(img):
    img = img.convert('P', palette=Image.ADAPTIVE, colors=15).convert("RGB")
    arr = Image.Image.getcolors(img)

    ans = []
    n = len(arr)
    for i in range(n - 1):
        for j in range(i + 1, n):
            f, s = arr[i][1], arr[j][1]
            ans.append(sqrt(pow(f[0] - s[0], 2) + pow(f[1] - s[1], 2) + pow(f[2] - s[2], 2)))
    return sorted(ans)


def percentage(num, guess, mode) -> float:
    if guess:
        s = num
        scale = 20 - mode
        while s > 20:
            s -= scale / 2
        s = (s - mode) / scale * 100
    else:
        s = 100 - (num / mode * 100)

    return s


def algo(file):
    img = Image.open(file, 'r')
    r, g, b = img.split()
    j = 1.45
    r = r.point(lambda i: i * j)
    g = g.point(lambda i: i * j)
    b = b.point(lambda i: i * j)
    result = Image.merge('RGB', (r, g, b))
    most = abs(min(distance(result)) - min(distance(img)))
    d, n = 9.0, 7.5  # custom n
    ok, ok_d, ok_n = True, most != d, most != n
    guess_d, guess_n = most > d, most > n
    guess = guess_d and guess_n
    per_d, per_n = percentage(most, guess_d, d), percentage(most, guess_n, n)
    avg = (per_d + per_n) / 2
    dist = max(per_d, per_n) - min(per_d, per_n)
    if guess:
        percent = avg + dist * 0.05
    else:
        if (ok_d and ok_n) or not ok_d:
            percent = avg - dist * 0.15
        else:
            ok = False
            percent = 0.0

    return [ok, guess, percent]


def neuro(file):
    prediction = CustomImageClassification()
    prediction.setModelTypeAsInceptionV3()
    prediction.setModelPath('model_graph(inception).h5')
    prediction.setJsonPath('model_class.json')
    prediction.loadModel(num_objects=2)

    predictions, probabilities = prediction.classifyImage(file, result_count=2)
    percent = probabilities[0]
    return [percent != 50.0, predictions[0] == 'yes', percent]


def calc(file):
    n = neuro(file)
    a = algo(file)
    ok = a[0] or n[0]
    if ok:
        if not a[0]:
            return [n[0], n[1], n[2]]
        if not n[0]:
            return [a[0], a[1], a[2]]

        if a[1] == n[1]:
            return [ok, a[1], (a[2]+n[2])/2]
        else:
            if not a[1]:
                return [n[0], n[1], n[2]]
            if not n[1]:
                return [a[0], a[1], a[2]]

    else:
        return [ok, False, 0.0]


folders = ['yes', 'no']

for f in folders:
    path = r'F:\\PyCharm\\NeuroMed\\CourseWork2\dataset\\initial\\' + f + '\\*'
    filenames = glob.glob(path)
    eCount, yCount, nCount = 0, 0, 0
    yPer, nPer = 0, 0
    for file in filenames:
        result = calc(file)
        if not result[0]:
            eCount += 1
        else:
            if result[1]:
                yCount += 1
                yPer += result[2]
            else:
                nCount += 1
                nPer += result[2]

    yAvg, nAvg = 0, 0
    if yCount != 0:
        yAvg = yPer / yCount
    if nCount != 0:
        nAvg = nPer / nCount
    print('Path: ', path)
    print('Yes: ', yCount, yAvg)
    print('No: ', nCount, nAvg)
    print('Error: ', eCount)
    print()
