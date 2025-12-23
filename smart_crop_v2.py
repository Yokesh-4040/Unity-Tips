#!/usr/bin/env python3
"""
Smart Card Cropper v2 - Enhanced edge detection for dark backgrounds.
Works with both light (marble) and dark (wooden) backgrounds.
"""

import sys
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

def find_card_by_edges(image_path, margin_percent=3):
    """
    Find card by detecting strong rectangular edges.
    Works better with dark backgrounds.

    Args:
        image_path: Path to input image
        margin_percent: Margin to add around card

    Returns:
        Crop coordinates (left, top, right, bottom)
    """
    # Load image
    img = Image.open(image_path)

    # Resize for faster processing
    max_dim = 1200
    if max(img.width, img.height) > max_dim:
        ratio = max_dim / max(img.width, img.height)
        work_size = (int(img.width * ratio), int(img.height * ratio))
        work_img = img.resize(work_size, Image.Resampling.LANCZOS)
    else:
        work_img = img.copy()
        ratio = 1.0

    # Convert to grayscale
    gray = work_img.convert('L')

    # Enhance contrast to make edges more visible
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2.0)

    # Apply strong edge detection
    edges = gray.filter(ImageFilter.FIND_EDGES)
    edges = edges.filter(ImageFilter.MaxFilter(3))  # Dilate edges

    # Convert to numpy
    edge_array = np.array(edges)

    # Find strong edges (top 15% of edge strengths)
    threshold = np.percentile(edge_array[edge_array > 0], 85)
    strong_edges = edge_array > threshold

    # Look for the rectangular card boundary
    # Cards have strong edges on all four sides

    # Analyze row by row - find rows with significant edge pixels
    row_edge_count = np.sum(strong_edges, axis=1)
    col_edge_count = np.sum(strong_edges, axis=0)

    # Find the main rectangular region
    # Look for continuous region with edge pixels
    min_edge_pixels_row = work_img.width * 0.08  # 8% of width
    min_edge_pixels_col = work_img.height * 0.08  # 8% of height

    edge_rows = row_edge_count > min_edge_pixels_row
    edge_cols = col_edge_count > min_edge_pixels_col

    # Find the largest continuous region
    edge_row_indices = np.where(edge_rows)[0]
    edge_col_indices = np.where(edge_cols)[0]

    if len(edge_row_indices) == 0 or len(edge_col_indices) == 0:
        print("⚠️  Could not detect card edges clearly")
        return fallback_center_crop(img)

    # Get boundaries
    top_work = edge_row_indices[0]
    bottom_work = edge_row_indices[-1]
    left_work = edge_col_indices[0]
    right_work = edge_col_indices[-1]

    # Refine by looking at edge density
    # The card should have dense edges at its boundaries
    detected_height = bottom_work - top_work
    detected_width = right_work - left_work

    # Check aspect ratio - cards are typically 1.3-1.5 tall
    detected_ratio = detected_height / detected_width if detected_width > 0 else 0

    if detected_ratio < 1.1 or detected_ratio > 1.8:
        print(f"⚠️  Aspect ratio {detected_ratio:.2f} seems off, adjusting...")

        # Use detected width, calculate proper height
        center_x = (left_work + right_work) // 2
        center_y = (top_work + bottom_work) // 2

        card_width = detected_width
        card_height = int(card_width * 1.4)  # Standard card ratio

        left_work = int(center_x - card_width / 2)
        right_work = int(center_x + card_width / 2)
        top_work = int(center_y - card_height / 2)
        bottom_work = int(center_y + card_height / 2)

    # Add margin
    margin_h = int((bottom_work - top_work) * margin_percent / 100)
    margin_w = int((right_work - left_work) * margin_percent / 100)

    top_work = max(0, top_work - margin_h)
    bottom_work = min(work_img.height, bottom_work + margin_h)
    left_work = max(0, left_work - margin_w)
    right_work = min(work_img.width, right_work + margin_w)

    # Scale back to original coordinates
    left = int(left_work / ratio)
    top = int(top_work / ratio)
    right = int(right_work / ratio)
    bottom = int(bottom_work / ratio)

    # Ensure within bounds
    left = max(0, left)
    top = max(0, top)
    right = min(img.width, right)
    bottom = min(img.height, bottom)

    return (left, top, right, bottom)

def fallback_center_crop(img):
    """Fallback: center crop with reasonable margins"""
    margin = 0.18
    left = int(img.width * margin)
    top = int(img.height * margin)
    right = int(img.width * (1 - margin))
    bottom = int(img.height * (1 - margin))
    return (left, top, right, bottom)

def smart_crop_v2(input_path, output_path=None, margin=3):
    """
    Enhanced cropping that works with dark backgrounds.

    Args:
        input_path: Input image path
        output_path: Output path (None = overwrite)
        margin: Margin percentage

    Returns:
        Output path
    """
    if output_path is None:
        output_path = input_path

    # Load image
    img = Image.open(input_path)
    print(f"📸 Original: {img.width}x{img.height} ({img.width*img.height/1000000:.1f}MP)")

    # Detect card using enhanced edge detection
    print("🤖 AI detecting card with enhanced edge analysis...")
    left, top, right, bottom = find_card_by_edges(input_path, margin)

    # Crop
    cropped = img.crop((left, top, right, bottom))
    ratio = cropped.height / cropped.width

    print(f"✂️  Detected: ({left}, {top}) → ({right}, {bottom})")
    print(f"📐 Cropped: {cropped.width}x{cropped.height} (ratio: {ratio:.2f}:1)")

    # Check if ratio is reasonable
    if ratio < 1.2 or ratio > 1.6:
        print(f"⚠️  Ratio {ratio:.2f} may need adjustment")
        print("💡 Try: python3 smart_crop_v2.py [input] [output] [margin]")
        print("    Example: python3 smart_crop_v2.py input.png output.png 5")

    # Save
    cropped.save(output_path, quality=95, optimize=True)

    # Stats
    import os
    original_mb = os.path.getsize(input_path) / 1024 / 1024
    cropped_mb = os.path.getsize(output_path) / 1024 / 1024
    savings = ((original_mb - cropped_mb) / original_mb) * 100 if original_mb > 0 else 0

    print(f"💾 Saved: {output_path}")
    print(f"📊 Size: {original_mb:.2f}MB → {cropped_mb:.2f}MB ({savings:.1f}% smaller)")

    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🎴 Smart Card Cropper v2 - Works with dark backgrounds!")
        print("\nUsage: python3 smart_crop_v2.py <input> [output] [margin%]")
        print("\nExamples:")
        print("  python3 smart_crop_v2.py Tip_012/Tip012.png")
        print("  python3 smart_crop_v2.py Tip_012/Tip012.png Tip_012/cropped.png")
        print("  python3 smart_crop_v2.py Tip_012/Tip012.png Tip_012/cropped.png 5")
        print("\nThis version uses edge detection and works better with:")
        print("  ✓ Dark wooden backgrounds")
        print("  ✓ Light marble backgrounds")
        print("  ✓ Mixed lighting conditions")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else input_path
    margin = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    smart_crop_v2(input_path, output_path, margin)
    print("\n✨ Done! Enhanced cropping complete.")
