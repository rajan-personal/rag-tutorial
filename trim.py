import sys

sys.setrecursionlimit(100000)

with open('console_output.txt', 'w') as f:
    sys.stdout = f

    from PIL import Image

    img = Image.open("new_sample.png")
    if img.mode != 'RGB':
        img = img.convert('RGB')

    def mark_pixel(x1, y1, color):
        if f'{x1}_{y1}' in done:
            return

        img.putpixel((x1, y1), color)
        done.append(f'{x1}_{y1}')

        try:
            if x1 > 0 and f'{x1 - 1}_{y1}' not in done and img.getpixel((x1 - 1, y1)) in [white, color]:
                mark_pixel(x1 - 1, y1, color)

            if y1 > 0 and f'{x1}_{y1 - 1}' not in done and img.getpixel((x1, y1 - 1)) in [white, color]:
                mark_pixel(x1, y1 - 1, color)

            if x1 < img.width - 1 and f'{x1 + 1}_{y1}' not in done and img.getpixel((x1 + 1, y1)) in [white, color]:
                mark_pixel(x1 + 1, y1, color)

            if y1 < img.height - 1 and f'{x1}_{y1 + 1}' not in done and img.getpixel((x1, y1 + 1)) in [white, color]:
                mark_pixel(x1, y1 + 1, color)
        except RecursionError:
            print(f'Recursion limit reached at pixel: ({x1}, {y1})')

    x = 0
    y = 0
    done = []
    white = (255, 255, 255)
    red = (255, 0, 0)
    mark_pixel(x, y, red)
    img.save('new_sample2.png')

sys.stdout = sys.__stdout__