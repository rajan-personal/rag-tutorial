from PIL import Image
import numpy as np
import torch
from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
import time
import os
import warnings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Set cache directory
os.environ['HF_HOME'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model_cache')
os.makedirs(os.environ['HF_HOME'], exist_ok=True)

def load_image(filename):
    """
    Load and convert image to grayscale
    """
    image = Image.open(filename).convert('L')
    # Convert to 3-channel by duplicating grayscale
    image_3ch = Image.merge('RGB', (image, image, image))
    return image_3ch

def initialize_model():
    """
    Initialize the CLIPSeg model and processor
    """
    print("Starting model initialization...")
    start_time = time.time()
    
    processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
    print(f"Processor initialization took {time.time() - start_time:.2f} seconds")
    
    model_start_time = time.time()
    model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")
    print(f"Model initialization took {time.time() - model_start_time:.2f} seconds")
    
    print(f"Total initialization time: {time.time() - start_time:.2f} seconds")
    return processor, model

def get_segmentation_masks(image, prompts, processor, model):
    """
    Get segmentation masks for given image and prompts
    """
    # Prepare inputs
    inputs = processor(text=prompts, 
                      images=[image] * len(prompts), 
                      padding=True,
                      truncation=True,
                      return_tensors="pt")
    
    # Get predictions
    with torch.no_grad():
        outputs = model(**inputs)
    
    preds = outputs.logits
    
    # Convert predictions to PIL images
    segmentation_masks = []
    for i in range(len(prompts)):
        # Convert tensor to numpy array and scale to 0-255
        mask = torch.sigmoid(preds[i]).numpy()
        mask = (mask * 255).astype(np.uint8)
        # Convert to PIL Image
        mask_image = Image.fromarray(mask)
        segmentation_masks.append(mask_image)
    
    return segmentation_masks

def apply_threshold(image, threshold=70):
    """
    Apply threshold to convert image to binary (black and white)
    """
    bw_img = image.convert('L')
    
    for x in range(bw_img.width):
        for y in range(bw_img.height):
            if bw_img.getpixel((x, y)) < threshold:
                bw_img.putpixel((x, y), 0)
            else:
                bw_img.putpixel((x, y), 255)
    
    return bw_img

def find_boundaries(bw_img):
    """
    Find the boundaries and center point of white pixels in a binary image
    """
    # Initialize the boundary values
    left_most = bw_img.width   # Start with maximum possible value
    right_most = 0            # Start with minimum possible value
    top_most = bw_img.height  # Start with maximum possible value
    bottom_most = 0          # Start with minimum possible value

    # Scan through all pixels
    for x in range(bw_img.width):
        for y in range(bw_img.height):
            if bw_img.getpixel((x, y)) == 255:  # If we find a white pixel
                # Update boundaries
                left_most = min(left_most, x)
                right_most = max(right_most, x)
                top_most = min(top_most, y)
                bottom_most = max(bottom_most, y)

    # Calculate center coordinates
    center_x = (left_most + right_most) // 2
    center_y = (top_most + bottom_most) // 2

    return {
        'left': left_most,
        'right': right_most,
        'top': top_most,
        'bottom': bottom_most,
        'center': (center_x, center_y)
    }

def process_segmentation_mask(mask, threshold=70):
    """
    Process a segmentation mask to find boundaries and center
    """
    bw_img = apply_threshold(mask, threshold)
    boundaries = find_boundaries(bw_img)
    return bw_img, boundaries

def crop_square_region(image, boundaries, padding=10):
    """
    Crop a square region from the image based on boundaries
    Args:
        image: PIL Image to crop
        boundaries: Dictionary containing left, right, top, bottom coordinates
        padding: Optional padding around the region (default: 10 pixels)
    Returns:
        Cropped PIL Image
    """
    left = max(0, boundaries['left'] - padding)
    right = min(image.width, boundaries['right'] + padding)
    top = max(0, boundaries['top'] - padding)
    bottom = min(image.height, boundaries['bottom'] + padding)
    
    # Make the crop region square by taking the larger dimension
    width = right - left
    height = bottom - top
    max_dim = max(width, height)
    
    # Adjust coordinates to make a square while keeping the region centered
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2
    
    left = max(0, center_x - max_dim // 2)
    right = min(image.width, center_x + max_dim // 2)
    top = max(0, center_y - max_dim // 2)
    bottom = min(image.height, center_y + max_dim // 2)
    
    return image.crop((left, top, right, bottom))

def main(image_path, prompts):
    """
    Main function to process image and get segmentation masks
    """
    # Load image
    image = load_image(image_path)
    
    # Initialize model
    processor, model = initialize_model()
    
    # Get segmentation masks
    masks = get_segmentation_masks(image, prompts, processor, model)
    
    return masks

if __name__ == "__main__":
    # Example usage
    filename = os.getenv('STEP_0_FILENAME', 'Test_Sample/pass.png')  # Use environment variable with fallback
    print(f"Using filename: {filename}")
    print(f"File exists: {os.path.exists(filename)}")
    print(f"Working directory: {os.getcwd()}")
    prompts = ["black color", "squares"]
    
    # Load original image once
    original_image = load_image(filename)
    masks = main(filename, prompts)
    
    # Process each mask
    for i, mask in enumerate(masks):
        bw_img, boundaries = process_segmentation_mask(mask)
        print(f"\nResults for prompt: '{prompts[i]}'")
        print(f"Left most white pixel: x = {boundaries['left']}")
        print(f"Right most white pixel: x = {boundaries['right']}")
        print(f"Top most white pixel: y = {boundaries['top']}")
        print(f"Bottom most white pixel: y = {boundaries['bottom']}")
        print(f"Center point: x = {boundaries['center'][0]}, y = {boundaries['center'][1]}")
        
        # Crop and save the detected region
        cropped_img = crop_square_region(original_image, boundaries)
        output_filename = f"processed_0_{prompts[i].replace(' ', '_')}.png"
        cropped_img.save(output_filename)
        print(f"Saved cropped image to: {output_filename}")