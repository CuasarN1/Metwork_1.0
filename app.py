from math import sqrt
from PIL import Image
import PySimpleGUI as sg
from os import path
import tensorflow as tf


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
    return path.isfile(val)


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


layout = [
    [sg.Text('Файл'), sg.InputText(), sg.FileBrowse('Открыть'), sg.Button('Показать', key='-SHOW-')],
    [sg.Output(key='-OUT-', size=(69, 20))],
    [sg.Button('Анализ', key='-BTN-', )
     , sg.Checkbox('Ночной режим')
     , sg.Text(60 * ' '), sg.Button('Очистить', key='-CLR-')]
]

window = sg.Window('Меню', layout)

while True:
    event, values = window.read()
    # print(event, values) # debug
    if event in (None, 'Exit'):
        break
    if event == '-CLR-':
        window['-OUT-'].update('')
    if event == '-SHOW-':
        if not values[0]:
            warn('file')
        else:
            if not exist(values[0]):
                warn('exist')
            else:
                try:
                    Image.open(values[0], 'r').show()
                except Exception as e:
                    sg.popup_error('Critical error!', e)
                    break

    if event == '-BTN-':
        if not values[0]:
            warn('file')
        else:
            if not exist(values[0]):
                warn('exist')
            else:
                try:
                    if values[1]:
                        mode = 7.5
                    else:
                        mode = 9.0
                    img = Image.open(values[0], 'r')
                    r, g, b = img.split()
                    j = 1.45
                    r = r.point(lambda i: i * j)
                    g = g.point(lambda i: i * j)
                    b = b.point(lambda i: i * j)
                    result = Image.merge('RGB', (r, g, b))
                    most = abs(min(distance(result)) - min(distance(img)))
                    print('Файл:', values[0])
                    print('\nПредположение:', end=' ')
                    if most == mode:
                        print('не удалось сделать предположение по данной фотографии\n')
                        print('Попробуйте переключить режим или загрузите другое фото.')
                    else:
                        if most > mode:
                            print('на снимке скорее всего ЕСТЬ отклонение от нормы')
                            guess = True
                        else:
                            print('на снимке скорее всего НЕТ отклонения от нормы')
                            guess = False
                        print('\nРежим:', end=' ')
                        if values[1]:
                            print('ночной')
                        else:
                            print('дневной')
                        print('\nВероятность предположения:', percentage(most, guess, mode))  # , round(most, 3))
                    print(69 * '_', end='\n\n')

                except Exception as e:
                    # tb = traceback.format_exc()  # debug
                    sg.popup_error('Critical error!', e)  # ('Critical error!', e, tb)
                    break
