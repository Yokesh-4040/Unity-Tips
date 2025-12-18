#!/usr/bin/env python3
"""
Automatic card cropping using brightness-based detection.
Finds the dark card rectangle against lighter backgrounds.
"""

import sys
from PIL import Image, ImageFilter
import numpy as np

def find_dark_rectangle(image_path, margin_percent=3):
    """
    Find the dark rectangular card in the image by analyzing brightness.

    Args:
        image_path: Path to input image
        margin_percent: Percentage margin to add around detected card

    Returns:
        Crop coordinates (left, top, right, bottom)
    """
    # Load and convert to grayscale
    img = Image.open(image_path)
    gray = img.convert('L')

    # Resize for faster processing
    max_dim = 800
    if max(gray.width, gray.height) > max_dim:
        ratio = max_dim / max(gray.width, gray.height)
        work_size = (int(gray.width * ratio), int(gray.height * ratio))
        gray_work = gray.resize(work_size, Image.Resampling.LANCZOS)
    else:
        gray_work = gray
        ratio = 1.0

    # Convert to numpy array
    arr = np.array(gray_work)

    # Calculate threshold to separate dark card from light background
    # The card is significantly darker than the marble background
    mean_brightness = np.mean(arr)
    std_brightness = np.std(arr)

    # Threshold: anything darker than mean - 1 std is likely the card
    threshold = mean_brightness - std_brightness * 0.8
    dark_mask = arr < threshold

    # Find the bounding box of dark regions
    # Use row and column sums to find where dark pixels are concentrated
    row_dark_count = np.sum(dark_mask, axis=1)
    col_dark_count = np.sum(dark_mask, axis=0)

    # Find continuous regions with significant dark pixels
    # Card should have consistent dark pixels across rows/columns
    min_dark_pixels_row = gray_work.width * 0.15  # At least 15% of width
    min_dark_pixels_col = gray_work.height * 0.15  # At least 15% of height

    dark_rows = np.where(row_dark_count > min_dark_pixels_row)[0]
    dark_cols = np.where(col_dark_count > min_dark_pixels_col)[0]

    if len(dark_rows) == 0 or len(dark_cols) == 0:
        print("⚠️  Could not detect card automatically, using center crop")
        # Fallback: center crop with reasonable margins
        margin = 0.15
        left = int(img.width * margin)
        top = int(img.height * margin)
        right = int(img.width * (1 - margin))
        bottom = int(img.height * (1 - margin))
        return (left, top, right, bottom)

    # Get the bounding box
    top_work = dark_rows[0]
    bottom_work = dark_rows[-1]
    left_work = dark_cols[0]
    right_work = dark_cols[-1]

    # Add margin (percentage of detected size)
    detected_height = bottom_work - top_work
    detected_width = right_work - left_work

    margin_h = int(detected_height * margin_percent / 100)
    margin_w = int(detected_width * margin_percent / 100)

    top_work = max(0, top_work - margin_h)
    bottom_work = min(gray_work.height, bottom_work + margin_h)
    left_work = max(0, left_work - margin_w)
    right_work = min(gray_work.width, right_work + margin_w)

    # Scale back to original image coordinates
    left = int(left_work / ratio)
    top = int(top_work / ratio)
    right = int(right_work / ratio)
    bottom = int(bottom_work / ratio)

    # Verify aspect ratio is reasonable for a card (1.2 to 1.6)
    aspect_ratio = (bottom - top) / (right - left) if (right - left) > 0 else 0

    if aspect_ratio < 1.1 or aspect_ratio > 1.8:
        print(f"⚠️  Unusual aspect ratio detected: {aspect_ratio:.2f}")
        # Try to fix by adjusting based on standard card ratio (1.4)
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        # Use detected width, calculate proper height
        card_width = right - left
        card_height = int(card_width * 1.4)

        left = int(center_x - card_width / 2)
        right = int(center_x + card_width / 2)
        top = int(center_y - card_height / 2)
        bottom = int(center_y + card_height / 2)

        # Ensure within bounds
        left = max(0, left)
        right = min(img.width, right)
        top = max(0, top)
        bottom = min(img.height, bottom)

    return (left, top, right, bottom)

def auto_crop_card(input_path, output_path=None, margin=3):
    """
    Automatically detect and crop card with no human input.

    Args:
        input_path: Input image path
        output_path: Output path (None = overwrite)
        margin: Margin percentage around card

    Returns:
        Output path
    """
    if output_path is None:
        output_path = input_path

    # Load image
    img = Image.open(input_path)
    print(f"📸 Original: {img.width}x{img.height} ({img.width*img.height/1000000:.1f}MP)")

    # Detect card
    print("🤖 AI detecting card boundaries...")
    left, top, right, bottom = find_dark_rectangle(input_path, margin)

    # Crop
    cropped = img.crop((left, top, right, bottom))
    ratio = cropped.height / cropped.width

    print(f"✂️  Detected: ({left}, {top}) → ({right}, {bottom})")
    print(f"📐 Cropped: {cropped.width}x{cropped.height} (ratio: {ratio:.2f}:1)")

    # Save
    cropped.save(output_path, quality=95, optimize=True)

    # Stats
    import os
    original_mb = os.path.getsize(input_path) / 1024 / 1024
    cropped_mb = os.path.getsize(output_path) / 1024 / 1024
    savings = ((original_mb - cropped_mb) / original_mb) * 100

    print(f"💾 Saved: {output_path}")
    print(f"📊 Size: {original_mb:.2f}MB → {cropped_mb:.2f}MB ({savings:.1f}% smaller)")

    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🎴 Auto Card Cropper - AI-powered, zero human input")
        print("\nUsage: python auto_crop_card.py <input> [output] [margin%]")
        print("\nExamples:")
        print("  python auto_crop_card.py Tip_011/Tip011.png")
        print("  python auto_crop_card.py Tip_011/Tip011.png Tip_011/cropped.png")
        print("  python auto_crop_card.py Tip_011/Tip011.png Tip_011/cropped.png 5")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    margin = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    auto_crop_card(input_path, output_path, margin)
    print("\n✨ Done! Card cropped automatically with AI.")
