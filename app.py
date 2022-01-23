from math import sqrt
from PIL import Image
import PySimpleGUI as sg
import os
from imageai.Classification.Custom import CustomImageClassification


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


def exist(val) -> bool:
    try:
        return os.path.isfile(val)
    except Exception as e:
        sg.popup_error('Critical error!', e)


def warn(error):
    if error == 'file':
        print('Выберите файл!\n')
    elif error == 'exist':
        print('Файл по указанному пути не найден!\n')


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


def neuro(file):
    prediction = CustomImageClassification()
    prediction.setModelTypeAsInceptionV3()
    prediction.setModelPath('model_graph(inception).h5')
    prediction.setJsonPath('model_class.json')
    prediction.loadModel(num_objects=2)

    predictions, probabilities = prediction.classifyImage(file, result_count=2)
    percent = probabilities[0]
    return [percent != 50.0, predictions[0] == 'yes', percent]


def algo(file):
    img = Image.open(file, 'r')
    r, g, b = img.split()
    j = 1.45
    r = r.point(lambda i: i * j)
    g = g.point(lambda i: i * j)
    b = b.point(lambda i: i * j)
    result = Image.merge('RGB', (r, g, b))
    most = abs(min(distance(result)) - min(distance(img)))
    d, n = 9.0, 7.5
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


def calc(file):
    n = neuro(file)
    a = algo(file)
    ok = a[0] or n[0]
    ok = False
    if ok:
        if not a[0]:
            print_r(n[0], n[1], n[2], file, True)
        elif not n[0]:
            print_r(a[0], a[1], a[2], file, False)

        elif a[1] == n[1]:
            print_r(ok, a[1], (a[2] + n[2]) / 2, file)
        else:
            if not a[1]:
                print_r(n[0], n[1], n[2], file)
            if not n[1]:
                print_r(a[0], a[1], a[2], file)

    else:
        print_r(ok, False, 0.0, file)


def print_r(ok, res, percent, f, mode=True):
    text = window['-OUT-'].get()
    window['-OUT-'].update('')
    print(text.replace('Подождите, пожалуйста...\n', '').replace('Подождите, пожалуйста...', '')
              .replace('Выберите файл!\n\n', '').replace('Файл по указанному пути не найден!\n\n', ''), end='')
    print('File:', f)
    print('\nGuess:', end=' ')
    if not ok:
        # print('не удалось сделать предположение по данной фотографии\n')
        # print('Загрузите другое фото.')
        print('unable to detect the image\n')
        print('Please, check the image quality.')
    else:
        if res:
            # print('на снимке скорее всего ЕСТЬ отклонение от нормы')
            print('image contains an abnormalities')
        else:
            # print('на снимке скорее всего НЕТ отклонения от нормы')
            print('image does not contain abnormalities')
        print('\nPercentage:', str(round(percent, 3)) + '%')
        if mode is True:
            print('\nAnalysis mode: neural (default)')
        elif mode is False:
            print('\nAnalysis mode: image correction')
    print(62 * '_', end='\n\n')


layout = [
    [sg.Text('File'), sg.InputText(), sg.FileBrowse('Open'), sg.Button('Show', key='-SHOW-')],
    [sg.Output(key='-OUT-', size=(62, 20))],
    [sg.Button('Analyse', key='-BTN-', ), sg.Text(84 * ' '), sg.Button('Clear', key='-CLR-')]
]

window = sg.Window('Metwork', layout)

while True:
    event, values = window.read()
    file = values[0]
    # print(event, values) # debug
    if event in (None, 'Exit'):
        break
    if event == '-CLR-':
        window['-OUT-'].update('')
    if event == '-SHOW-':
        if not file:
            warn('file')
        else:
            if not exist(file):
                warn('exist')
            else:
                try:
                    Image.open(file, 'r').show()
                except Exception as e:
                    sg.popup_error('Critical error!', e)
                    break

    if event == '-BTN-':
        if not file:
            warn('file')
        else:
            if not exist(file):
                warn('exist')
            else:
                try:
                    print('Подождите, пожалуйста...', end='')
                    calc(file)

                except Exception as e:
                    # tb = traceback.format_exc()  # debug
                    sg.popup_error('Critical error!', e)  # ('Critical error!', e, tb)
                    break
