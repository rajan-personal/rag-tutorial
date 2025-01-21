from PIL import Image

img = Image.open("processed_0_squares.png")
bw_img = img.convert('L')

THRESHOLD = 90
for x in range(bw_img.width):
    for y in range(bw_img.height):
        if bw_img.getpixel((x, y)) < THRESHOLD:
            bw_img.putpixel((x, y), 0)
        else:
            bw_img.putpixel((x, y), 255)
            
bw_img.save('processed_1_squares.png')