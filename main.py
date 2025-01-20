# save image in memory


from PIL import Image
from io import BytesIO

img = Image.open("sample.png")

# convert into black and white
bw_img = img.convert('L')  # 'L' mode means single channel grayscale


# # print each pixel value
# for x in range(bw_img.width):
#     for y in range(bw_img.height):
#         print(bw_img.getpixel((x, y)), end=' ')
#     print()
        
THRESHOLD = 90
for x in range(bw_img.width):
    for y in range(bw_img.height):
        if bw_img.getpixel((x, y)) < THRESHOLD:
            bw_img.putpixel((x, y), 0)
        else:
            bw_img.putpixel((x, y), 255)
            
bw_img.save('new_sample.png')