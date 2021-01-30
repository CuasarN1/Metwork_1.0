from PIL import Image

# opening a  image
im = Image.open(r"yes/2020_02_17_11_59_22.png").convert("L")

# getting colors
# multiband images (RBG)
im1 = Image.Image.getcolors(im, maxcolors=256)

sum = 0
for e in im1:
    sum += e[0]

print(sum)
print(len(im1))
print(im1)