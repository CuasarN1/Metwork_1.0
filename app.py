from math import sqrt
from PIL import Image
import PySimpleGUI as sg
import os
from imageai.Classification.Custom import CustomImageClassification


def diff(arr):
    ans = []
    n = len(arr)
    for i in range(n - 1):
        for j in range(i + 1, n):
            f, s = arr[i][1], arr[j][1]
            ans.append(sqrt(pow(f[0] - s[0], 2) + pow(f[1] - s[1], 2) + pow(f[2] - s[2], 2)))
    return ans


def distance(img):
    img = img.convert('P', palette=Image.ADAPTIVE, colors=15).convert("RGB")
    colors = Image.Image.getcolors(img)

    return sorted(diff(colors))


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


def percentage(num, guess, mode) -> str:
    if guess:
        s = num
        scale = 20 - mode
        while s > 20:
            s -= scale / 2
        s = (s - mode) / scale * 100
    else:
        s = 100 - (num / mode * 100)

    return str(round(s, 3)) + '%'


def neuro(file):
    prediction = CustomImageClassification()
    prediction.setModelTypeAsResNet50()
    prediction.setModelPath('model_graph(2nd).h5')
    prediction.setJsonPath('model_class.json')
    prediction.loadModel(num_objects=2)

    predictions, probabilities = prediction.classifyImage(file, result_count=2)
    result = probabilities[0]
    if result != 100.0:
        print_r(result != 50.0, predictions[0] == 'yes', result, True, file)
    else:
        algo(file)


def algo(file):
    img = Image.open(file, 'r')
    r, g, b = img.split()
    j = 1.45
    r = r.point(lambda i: i * j)
    g = g.point(lambda i: i * j)
    b = b.point(lambda i: i * j)
    result = Image.merge('RGB', (r, g, b))
    most = abs(min(distance(result)) - min(distance(img)))
    mode = 7.5  # 9.0 (day)
    guess = most > mode
    print_r(most != mode, guess, percentage(most, guess, mode), False, file)


def print_r(ok, res, percent, mode, f):
    text = window['-OUT-'].get()
    window['-OUT-'].update('')
    print(text.replace('Подождите, пожалуйста...\n', '').replace('Подождите, пожалуйста...', '')
              .replace('Выберите файл!\n\n', '').replace('Файл по указанному пути не найден!\n\n', ''), end='')
    print('Файл:', f)
    print('\nПредположение:', end=' ')
    if not ok:
        print('не удалось сделать предположение по данной фотографии\n')
        print('Попробуйте переключить режим или загрузите другое фото.')
    else:
        if res:
            print('на снимке скорее всего ЕСТЬ отклонение от нормы')
        else:
            print('на снимке скорее всего НЕТ отклонения от нормы')
        print('\nВероятность предположения:', percent)
        print('\nРежим анализа: ', end='')
        if mode:
            print('нейронный')
        else:
            print('алгоритмический')
        print(69 * '_', end='\n\n')


layout = [
    [sg.Text('Файл'), sg.InputText(), sg.FileBrowse('Открыть'), sg.Button('Показать', key='-SHOW-')],
    [sg.Output(key='-OUT-', size=(69, 20))],
    [sg.Button('Анализ', key='-BTN-', ), sg.Text(91 * ' '), sg.Button('Очистить', key='-CLR-')]
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
                    neuro(file)

                except Exception as e:
                    # tb = traceback.format_exc()  # debug
                    sg.popup_error('Critical error!', e)  # ('Critical error!', e, tb)
                    break
