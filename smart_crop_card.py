#!/usr/bin/env python3
"""
Smart card cropping using edge detection and contour analysis.
Automatically detects and crops developer cards with no human input.
"""

import sys
from PIL import Image, ImageFilter, ImageDraw, ImageStat
import numpy as np

def find_card_contour(image_path, debug=False):
    """
    Use edge detection and contour analysis to find the card.

    Args:
        image_path: Path to input image
        debug: If True, show detection steps

    Returns:
        Tuple of (left, top, right, bottom) crop coordinates
    """
    # Load image
    img = Image.open(image_path)
    original_size = (img.width, img.height)

    # Resize for faster processing (maintain aspect ratio)
    max_dimension = 1000
    if img.width > max_dimension or img.height > max_dimension:
        ratio = min(max_dimension / img.width, max_dimension / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        working_img = img.resize(new_size, Image.Resampling.LANCZOS)
        scale_factor = ratio
    else:
        working_img = img.copy()
        scale_factor = 1.0

    # Convert to grayscale
    gray = working_img.convert('L')

    # Enhance edges
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = edges.filter(ImageFilter.MaxFilter(5))  # Dilate edges

    # Convert to numpy for analysis
    edge_array = np.array(edges)

    # Find strong edges (potential card boundaries)
    threshold = np.percentile(edge_array, 90)  # Top 10% of edges
    strong_edges = edge_array > threshold

    # Find bounding box of strong edges
    rows = np.any(strong_edges, axis=1)
    cols = np.any(strong_edges, axis=0)

    row_indices = np.where(rows)[0]
    col_indices = np.where(cols)[0]

    if len(row_indices) == 0 or len(col_indices) == 0:
        print("Could not detect card edges. Using center crop.")
        # Fallback to center crop
        margin_h = int(working_img.height * 0.15)
        margin_w = int(working_img.width * 0.20)
        return (margin_w, margin_h,
                working_img.width - margin_w, working_img.height - margin_h,
                scale_factor)

    # Get initial boundaries
    top, bottom = row_indices[0], row_indices[-1]
    left, right = col_indices[0], col_indices[-1]

    # Refine by finding the largest rectangle of edges
    # (card typically has strong edges on all sides)
    height = bottom - top
    width = right - left

    # Add smart padding (proportional to card size)
    padding_h = int(height * 0.02)  # 2% padding
    padding_w = int(width * 0.02)

    top = max(0, top - padding_h)
    bottom = min(working_img.height, bottom + padding_h)
    left = max(0, left - padding_w)
    right = min(working_img.width, right + padding_w)

    # Ensure aspect ratio is reasonable for a card (roughly 2:3 or 3:4)
    detected_ratio = (bottom - top) / (right - left) if (right - left) > 0 else 0

    if detected_ratio < 1.2 or detected_ratio > 2.0:
        # Aspect ratio seems off, use more conservative crop
        print(f"Detected aspect ratio {detected_ratio:.2f} seems unusual, adjusting...")

        # Assume card is roughly 1.4:1 ratio (height:width)
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        # Use the width as reference
        card_width = min(right - left, working_img.width * 0.6)
        card_height = card_width * 1.4

        left = int(center_x - card_width / 2)
        right = int(center_x + card_width / 2)
        top = int(center_y - card_height / 2)
        bottom = int(center_y + card_height / 2)

        # Clamp to image bounds
        left = max(0, left)
        right = min(working_img.width, right)
        top = max(0, top)
        bottom = min(working_img.height, bottom)

    return (left, top, right, bottom, scale_factor)

def crop_card_smart(input_path, output_path=None):
    """
    Automatically detect and crop card from image.

    Args:
        input_path: Path to input image
        output_path: Path for output (None = overwrite input)

    Returns:
        Path to cropped image
    """
    if output_path is None:
        output_path = input_path

    # Load original image
    img = Image.open(input_path)
    print(f"📸 Original image size: {img.width}x{img.height}")

    # Detect card boundaries
    print("🔍 Detecting card boundaries...")
    left, top, right, bottom, scale = find_card_contour(input_path)

    # Scale coordinates back to original image size
    left = int(left / scale)
    top = int(top / scale)
    right = int(right / scale)
    bottom = int(bottom / scale)

    print(f"✂️  Cropping to: ({left}, {top}) -> ({right}, {bottom})")

    # Crop
    cropped = img.crop((left, top, right, bottom))
    cropped_ratio = cropped.height / cropped.width

    print(f"✅ Cropped size: {cropped.width}x{cropped.height} (ratio: {cropped_ratio:.2f})")

    # Save with optimization
    cropped.save(output_path, quality=95, optimize=True)

    # Show file size reduction
    import os
    original_size = os.path.getsize(input_path) / 1024 / 1024  # MB
    cropped_size = os.path.getsize(output_path) / 1024 / 1024
    reduction = ((original_size - cropped_size) / original_size) * 100 if original_size > 0 else 0

    print(f"💾 Saved to: {output_path}")
    print(f"📊 File size: {original_size:.2f}MB → {cropped_size:.2f}MB ({reduction:.1f}% reduction)")

    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python smart_crop_card.py <input_image> [output_image]")
        print("Example: python smart_crop_card.py Tip_011/Tip011.png")
        print("         python smart_crop_card.py Tip_011/Tip011.png Tip_011/Tip011_cropped.png")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path

    crop_card_smart(input_path, output_path)
    print("\n✨ Done! Card cropped successfully.")
