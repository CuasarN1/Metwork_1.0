import os
import glob


path = 'dataset/'
f = ['no/', 'yes/']
cnt = 0
for folder in f:
    files = glob.glob(path+folder + '*.png')
    for i, file in enumerate(files):
        j = i + 1
        cnt += 1
        # print(j, file)
        os.rename(file, path + folder + str(j//10) + str(j % 10) + '.png')

print(cnt)
