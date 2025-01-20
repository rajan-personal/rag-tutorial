from PIL import Image
import numpy as np
from collections import deque

def flood_fill(img, start_pos, color):
    width, height = img.size
    img_array = np.array(img)
    white = np.array([255, 255, 255])
    
    queue = deque([start_pos])
    done = set()
    
    while queue:
        x, y = queue.popleft()
        if (x, y) in done:
            continue
            
        img_array[y, x] = color
        done.add((x, y))
        
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if (0 <= nx < width and 
                0 <= ny < height and 
                (nx, ny) not in done and 
                np.array_equal(img_array[ny, nx], white)):
                queue.append((nx, ny))
    
    return Image.fromarray(img_array)

# Main processing
img = Image.open("new_sample.png")
if img.mode != 'RGB':
    img = img.convert('RGB')

white = (255, 255, 255)
red = (255, 0, 0)

# Process starting from top-left corner
img = flood_fill(img, (0, 0), red)
img.save('new_sample2.png')