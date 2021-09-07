from PIL import Image
import glob


path = 'dataset/no/'
All = False

files = glob.glob(path + '*.png')
if All:
    names = [file.split('\\')[1].replace('.png', '') for file in files]
else:
    files = [file for file in files if '_' in file]
    del files[1::2]
    names = [file.split('\\')[1].replace('.png', '') for file in files]
length = len(files)
cnt = 0
for i in range(length-1):
    img1 = Image.open(files[i])
    for j in range(i+1, length):
        img2 = Image.open(files[j])
        image = Image.blend(img1, img2, 0.5)
        image.save(path+names[j]+'_'+names[i]+'.png')
        cnt += 1

print(cnt)
