#!/usr/bin/env python3
"""
Simple Frame Screenshot Styler
Adds a clean white frame with rounded corners to screenshots
"""

import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw
import sys

class SimpleFrameStyler:
    def __init__(self):
        # Frame settings
        self.frame_color = (255, 255, 255)  # White
        self.frame_width = 80  # Wider frame by default
        self.corner_radius = 20  # Rounded corners
        
    def create_rounded_mask(self, size, radius):
        """Create a mask for rounded corners"""
        width, height = size
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        # Draw rounded rectangle
        draw.rounded_rectangle(
            [(0, 0), (width-1, height-1)],
            radius=radius,
            fill=255
        )
        
        return mask
        
    def add_white_frame(self, input_path, output_path):
        """Add white frame with rounded corners to screenshot"""
        # Open the original image
        original = Image.open(input_path).convert('RGBA')
        orig_width, orig_height = original.size
        
        # Calculate new dimensions
        new_width = orig_width + (self.frame_width * 2)
        new_height = orig_height + (self.frame_width * 2)
        
        # Create new image with white background
        new_img = Image.new('RGBA', (new_width, new_height), self.frame_color)
        
        # Paste original image in the center
        paste_x = self.frame_width
        paste_y = self.frame_width
        new_img.paste(original, (paste_x, paste_y), original)
        
        # Create rounded corners mask
        mask = self.create_rounded_mask((new_width, new_height), self.corner_radius)
        
        # Create output image with transparency
        output = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))
        output.paste(new_img, (0, 0))
        output.putalpha(mask)
        
        # Create final image with white background
        final = Image.new('RGBA', (new_width, new_height), self.frame_color)
        final.paste(output, (0, 0), output)
        
        # Save the result
        final.save(output_path, 'PNG')
        print(f"✅ Framed screenshot saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Add simple white frame with rounded corners to screenshots')
    parser.add_argument('input', help='Input screenshot file')
    parser.add_argument('-o', '--output', help='Output file (default: adds _framed suffix)')
    parser.add_argument('-w', '--width', type=int, default=80, help='Frame width in pixels (default: 80)')
    parser.add_argument('-r', '--radius', type=int, default=20, help='Corner radius in pixels (default: 20)')
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input)
        output_path = input_path.parent / f"{input_path.stem}_framed{input_path.suffix}"
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Process the image
    styler = SimpleFrameStyler()
    styler.frame_width = args.width
    styler.corner_radius = args.radius
    try:
        styler.add_white_frame(args.input, str(output_path))
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()