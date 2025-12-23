#!/usr/bin/env python3
"""
Manual Card Cropper - Full control over crop boundaries.
Specify exactly how much to crop from each side.
"""

import sys
from PIL import Image
import os

def manual_crop_percent(input_path, output_path, top=15, bottom=15, left=20, right=20):
    """
    Crop by percentage from each side.

    Args:
        input_path: Input image
        output_path: Output image
        top: % to crop from top (0-50)
        bottom: % to crop from bottom (0-50)
        left: % to crop from left (0-50)
        right: % to crop from right (0-50)
    """
    img = Image.open(input_path)
    width, height = img.size

    print(f"📸 Original: {width}x{height}")
    print(f"✂️  Cropping: {top}% top, {bottom}% bottom, {left}% left, {right}% right")

    # Calculate pixel coordinates
    crop_left = int(width * left / 100)
    crop_right = int(width * (100 - right) / 100)
    crop_top = int(height * top / 100)
    crop_bottom = int(height * (100 - bottom) / 100)

    # Validate
    if crop_left >= crop_right or crop_top >= crop_bottom:
        print("❌ Error: Crop percentages are too large, nothing would remain!")
        print(f"   Left: {crop_left}px, Right: {crop_right}px")
        print(f"   Top: {crop_top}px, Bottom: {crop_bottom}px")
        sys.exit(1)

    # Crop
    cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
    new_width, new_height = cropped.size
    ratio = new_height / new_width

    print(f"📐 Result: {new_width}x{new_height} (ratio: {ratio:.2f}:1)")

    # Check if ratio is good for a card
    if ratio < 1.2:
        print("⚠️  Warning: Too wide for a card (ratio < 1.2)")
        print("   Try: Increase top/bottom or decrease left/right")
    elif ratio > 1.6:
        print("⚠️  Warning: Too tall for a card (ratio > 1.6)")
        print("   Try: Decrease top/bottom or increase left/right")
    else:
        print("✅ Good aspect ratio for a card!")

    # Save
    cropped.save(output_path, quality=95, optimize=True)

    # Stats
    original_mb = os.path.getsize(input_path) / 1024 / 1024
    cropped_mb = os.path.getsize(output_path) / 1024 / 1024
    savings = ((original_mb - cropped_mb) / original_mb) * 100

    print(f"💾 Saved: {output_path}")
    print(f"📊 Size: {original_mb:.2f}MB → {cropped_mb:.2f}MB ({savings:.1f}% smaller)")

    return output_path

def manual_crop_pixels(input_path, output_path, top, bottom, left, right):
    """
    Crop by exact pixel amounts from each side.

    Args:
        input_path: Input image
        output_path: Output image
        top: pixels to crop from top
        bottom: pixels to crop from bottom
        left: pixels to crop from left
        right: pixels to crop from right
    """
    img = Image.open(input_path)
    width, height = img.size

    print(f"📸 Original: {width}x{height}")
    print(f"✂️  Cropping: {top}px top, {bottom}px bottom, {left}px left, {right}px right")

    # Calculate coordinates
    crop_left = left
    crop_right = width - right
    crop_top = top
    crop_bottom = height - bottom

    # Validate
    if crop_left >= crop_right or crop_top >= crop_bottom:
        print("❌ Error: Crop values are too large!")
        sys.exit(1)

    # Crop
    cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
    new_width, new_height = cropped.size
    ratio = new_height / new_width

    print(f"📐 Result: {new_width}x{new_height} (ratio: {ratio:.2f}:1)")

    if 1.2 <= ratio <= 1.6:
        print("✅ Good aspect ratio for a card!")
    else:
        print(f"⚠️  Ratio {ratio:.2f} may need adjustment")

    # Save
    cropped.save(output_path, quality=95, optimize=True)

    # Stats
    original_mb = os.path.getsize(input_path) / 1024 / 1024
    cropped_mb = os.path.getsize(output_path) / 1024 / 1024
    savings = ((original_mb - cropped_mb) / original_mb) * 100

    print(f"💾 Saved: {output_path}")
    print(f"📊 Size: {original_mb:.2f}MB → {cropped_mb:.2f}MB ({savings:.1f}% smaller)")

    return output_path

def show_dimensions(input_path):
    """Show image dimensions to help with manual cropping"""
    img = Image.open(input_path)
    print(f"📸 Image: {input_path}")
    print(f"📐 Dimensions: {img.width}x{img.height}")
    print(f"📊 Aspect ratio: {img.height/img.width:.2f}:1")
    print(f"💾 File size: {os.path.getsize(input_path)/1024/1024:.2f}MB")
    print()
    print("💡 Suggestions:")
    print("   For centered crop with margins:")
    print(f"   python3 manual_crop.py {input_path} output.png 15 15 20 20")
    print()
    print("   Or in pixels (example):")
    print(f"   python3 manual_crop.py {input_path} output.png {img.height//4} {img.height//4} {img.width//4} {img.width//4} --pixels")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("✂️  Manual Card Cropper - YOU control the crop!")
        print()
        print("Usage:")
        print("  1. Percentage mode (default):")
        print("     python3 manual_crop.py <input> <output> <top%> <bottom%> <left%> <right%>")
        print()
        print("  2. Pixel mode:")
        print("     python3 manual_crop.py <input> <output> <top_px> <bottom_px> <left_px> <right_px> --pixels")
        print()
        print("  3. Check image dimensions:")
        print("     python3 manual_crop.py <input> --info")
        print()
        print("Examples:")
        print("  # Crop 15% from top/bottom, 20% from left/right")
        print("  python3 manual_crop.py input.png output.png 15 15 20 20")
        print()
        print("  # Crop 500px from all sides")
        print("  python3 manual_crop.py input.png output.png 500 500 500 500 --pixels")
        print()
        print("  # Asymmetric crop: 20% top, 10% bottom, 25% left, 15% right")
        print("  python3 manual_crop.py input.png output.png 20 10 25 15")
        print()
        print("  # Get image info first")
        print("  python3 manual_crop.py input.png --info")
        print()
        print("Tips:")
        print("  • Start with percentages: 15 15 20 20 (good default)")
        print("  • Cards should have ratio 1.3-1.5 (height:width)")
        print("  • Use --info to see dimensions before cropping")
        print("  • Adjust values based on output ratio")
        sys.exit(0)

    input_path = sys.argv[1]

    # Info mode
    if len(sys.argv) == 3 and sys.argv[2] == "--info":
        show_dimensions(input_path)
        sys.exit(0)

    if len(sys.argv) < 6:
        print("❌ Error: Not enough arguments")
        print("Usage: python3 manual_crop.py <input> <output> <top> <bottom> <left> <right> [--pixels]")
        print("Or: python3 manual_crop.py <input> --info")
        sys.exit(1)

    output_path = sys.argv[2]
    top = int(sys.argv[3])
    bottom = int(sys.argv[4])
    left = int(sys.argv[5])
    right = int(sys.argv[6])

    # Check for pixel mode
    pixel_mode = len(sys.argv) > 7 and sys.argv[7] == "--pixels"

    print("✂️  Manual Card Cropper")
    print("=" * 50)

    if pixel_mode:
        manual_crop_pixels(input_path, output_path, top, bottom, left, right)
    else:
        manual_crop_percent(input_path, output_path, top, bottom, left, right)

    print()
    print("✨ Done! Check your cropped image:")
    print(f"   open {output_path}")
