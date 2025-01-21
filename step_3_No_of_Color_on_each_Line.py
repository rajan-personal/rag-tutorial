from PIL import Image, ImageDraw
import math

def get_boundary_point(center, angle, img_size):
    """Calculate the intersection of a line at a given angle with the image boundary."""
    cx, cy = center
    width, height = img_size
    radians = math.radians(angle)
    tan_theta = math.tan(radians)

    if 0 <= angle < 90 or 270 < angle < 360:
        x, y = width - 1, cy + int((width - 1 - cx) * tan_theta)
    else:
        x, y = 0, cy + int(-cx * tan_theta)

    if y < 0:
        y, x = 0, cx + int(-cy / tan_theta)
    elif y >= height:
        y, x = height - 1, cx + int((height - 1 - cy) / tan_theta)

    return max(0, min(x, width - 1)), max(0, min(y, height - 1))

def count_colors_along_line(img, start, end):
    """Count unique colors along a line between two points."""
    x1, y1 = start
    x2, y2 = end
    colors = set()
    num_points = max(abs(x2 - x1), abs(y2 - y1))
    for i in range(num_points + 1):
        x = int(x1 + i * (x2 - x1) / num_points)
        y = int(y1 + i * (y2 - y1) / num_points)
        colors.add(img.getpixel((x, y)))
    return len(colors)

def analyze_image(img_path, output_path):
    """Draw lines from the center of the image and count unique colors along each line."""
    img = Image.open(img_path).convert("RGB")
    width, height = img.size
    center = (width // 2, height // 2)

    draw_img = img.copy()
    draw = ImageDraw.Draw(draw_img)
    results = []

    for angle in range(360):
        end = get_boundary_point(center, angle, (width, height))
        draw.line((*center, *end), fill=(255, 0, 0), width=1)
        color_count = count_colors_along_line(img, center, end)
        results.append((angle, color_count))

    # for angle, count in results:
    #     print(f"Angle {angle}°: {count} colors")

    # if any angle has more or less then 6 colors print Error
    if any(count != 6 for _, count in results):
        print("Result Failed")
    else:
        print("Result Passed")

    draw_img.save(output_path)

# Main execution
analyze_image("processed_2_squares.png", "processed_3_squares.png")
