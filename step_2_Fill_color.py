from PIL import Image
import numpy as np
from collections import deque

def flood_fill(img_array, start_pos, fill_color):
    """Perform flood fill on the image array starting from the given position."""
    height, width, _ = img_array.shape
    white = np.array([255, 255, 255])
    queue = deque([start_pos])
    visited = set()

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue

        img_array[y, x] = fill_color
        visited.add((x, y))

        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited and np.array_equal(img_array[ny, nx], white):
                queue.append((nx, ny))

def find_white_pixel(img_array):
    """Find the first white pixel in the image array."""
    white = np.array([255, 255, 255])
    for y, row in enumerate(img_array):
        for x, pixel in enumerate(row):
            if np.array_equal(pixel, white):
                return (x, y)
    return None

def process_image(input_path, output_path):
    """Load the image, apply flood fill with gradient, and save the result."""
    img = Image.open(input_path).convert('RGB')
    img_array = np.array(img)

    green_gradient = 40
    shade = 0

    while True:
        start_pos = find_white_pixel(img_array)
        if not start_pos:
            break

        shade += 1
        fill_color = (0, max(0, 255 - green_gradient * shade), 0)
        flood_fill(img_array, start_pos, fill_color)

    Image.fromarray(img_array).save(output_path)

# Main execution
process_image("processed_1_squares.png", "processed_2_squares.png")
