# load image
# find center pixels of the image
# find colors in the image

from PIL import Image
import numpy as np

img = Image.open("new_sample.png")
img_array = np.array(img)
height, width = img_array.shape[:2]

if img.mode != 'RGB':
    img = img.convert('RGB')

center_x = width // 2
center_y = height // 2


# find colors in the image except black
colors = set()

for y in range(height):
    for x in range(width):
        colors.add(img.getpixel((x, y)))
            

print("colors: %d" % len(colors))

# remove black from colors
colors.remove((0, 0, 0))

print("colors: %d" % len(colors))