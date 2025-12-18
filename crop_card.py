#!/usr/bin/env python3
"""
Crop developer card images to remove background.
This script detects the card boundaries and crops to just the card.
"""

import sys
from PIL import Image, ImageFilter, ImageOps
import numpy as np

def find_card_boundaries(image_path, padding=20):
    """
    Detect card boundaries by finding the dark rectangle in the image.

    Args:
        image_path: Path to the input image
        padding: Extra pixels to add around detected boundaries

    Returns:
        Tuple of (left, top, right, bottom) coordinates
    """
    # Load image
    img = Image.open(image_path)

    # Convert to grayscale
    gray = img.convert('L')

    # Apply edge detection
    edges = gray.filter(ImageFilter.FIND_EDGES)

    # Convert to numpy array for processing
    img_array = np.array(gray)

    # Find dark regions (card is typically darker than background)
    # Threshold to find dark areas
    threshold = np.mean(img_array) - np.std(img_array) * 0.5
    binary = img_array < threshold

    # Find rows and columns with significant dark content
    row_has_dark = np.any(binary, axis=1)
    col_has_dark = np.any(binary, axis=0)

    # Find boundaries
    rows_with_content = np.where(row_has_dark)[0]
    cols_with_content = np.where(col_has_dark)[0]

    if len(rows_with_content) == 0 or len(cols_with_content) == 0:
        print("Could not detect card boundaries automatically.")
        return None

    top = max(0, rows_with_content[0] - padding)
    bottom = min(img.height, rows_with_content[-1] + padding)
    left = max(0, cols_with_content[0] - padding)
    right = min(img.width, cols_with_content[-1] + padding)

    return (left, top, right, bottom)

def crop_card(input_path, output_path=None, padding=20):
    """
    Crop the card from the image and save it.

    Args:
        input_path: Path to input image
        output_path: Path to save cropped image (if None, overwrites input)
        padding: Extra pixels around card
    """
    if output_path is None:
        output_path = input_path

    # Load original image
    img = Image.open(input_path)
    print(f"Original image size: {img.width}x{img.height}")

    # Find boundaries
    boundaries = find_card_boundaries(input_path, padding)

    if boundaries is None:
        print("Using manual crop approach...")
        # Fallback: crop to center with reasonable margins
        width, height = img.size
        left = int(width * 0.15)
        top = int(height * 0.05)
        right = int(width * 0.85)
        bottom = int(height * 0.95)
        boundaries = (left, top, right, bottom)

    left, top, right, bottom = boundaries
    print(f"Cropping to: left={left}, top={top}, right={right}, bottom={bottom}")

    # Crop the image
    cropped = img.crop(boundaries)
    print(f"Cropped image size: {cropped.width}x{cropped.height}")

    # Save
    cropped.save(output_path, quality=95, optimize=True)
    print(f"Saved cropped image to: {output_path}")

    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python crop_card.py <input_image> [output_image] [padding]")
        print("Example: python crop_card.py Tip_011/Tip011.png")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    padding = int(sys.argv[3]) if len(sys.argv) > 3 else 20

    crop_card(input_path, output_path, padding)
