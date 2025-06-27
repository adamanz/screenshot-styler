#!/usr/bin/env python3
"""
Terminal Screenshot Styler
Automatically adds a macOS-style terminal window frame to screenshots
"""

import argparse
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys

class TerminalStyler:
    def __init__(self):
        # Colors
        self.bg_color = (30, 30, 40)  # Dark background
        self.window_bg = (40, 42, 54)  # Terminal window background
        self.titlebar_bg = (60, 62, 74)  # Titlebar background
        self.button_red = (255, 95, 86)
        self.button_yellow = (255, 189, 46)
        self.button_green = (39, 201, 63)
        self.text_color = (200, 200, 200)
        
        # Dimensions
        self.padding = 40
        self.titlebar_height = 40
        self.button_size = 12
        self.button_spacing = 20
        self.button_start_x = 20
        self.corner_radius = 10
        
    def round_corner(self, radius, fill):
        """Creates a rounded corner"""
        corner = Image.new('RGBA', (radius * 2, radius * 2), (255, 255, 255, 0))
        draw = ImageDraw.Draw(corner)
        draw.pieslice((0, 0, radius * 2, radius * 2), 180, 270, fill=fill)
        return corner
    
    def create_rounded_rectangle(self, size, radius, fill):
        """Creates a rounded rectangle"""
        width, height = size
        rectangle = Image.new('RGBA', (width, height), fill)
        
        corner = self.round_corner(radius, fill)
        
        # Paste corners
        rectangle.paste(corner, (0, 0))
        rectangle.paste(corner.rotate(90), (0, height - radius * 2))
        rectangle.paste(corner.rotate(180), (width - radius * 2, height - radius * 2))
        rectangle.paste(corner.rotate(270), (width - radius * 2, 0))
        
        return rectangle
    
    def add_terminal_frame(self, input_path, output_path, title="Terminal"):
        """Add terminal frame to screenshot"""
        # Open the original image
        original = Image.open(input_path)
        orig_width, orig_height = original.size
        
        # Calculate new dimensions
        new_width = orig_width + (self.padding * 2)
        new_height = orig_height + self.titlebar_height + (self.padding * 2)
        
        # Create new image with background
        new_img = Image.new('RGBA', (new_width, new_height), self.bg_color)
        
        # Create terminal window
        terminal_width = orig_width + 2
        terminal_height = orig_height + self.titlebar_height + 2
        
        # Create rounded terminal window
        terminal_window = self.create_rounded_rectangle(
            (terminal_width, terminal_height), 
            self.corner_radius, 
            self.window_bg
        )
        
        # Draw titlebar
        draw = ImageDraw.Draw(terminal_window)
        
        # Titlebar background
        draw.rectangle(
            [(0, self.corner_radius), (terminal_width, self.titlebar_height)],
            fill=self.titlebar_bg
        )
        
        # Draw window buttons
        button_y = self.titlebar_height // 2
        
        # Red button (close)
        draw.ellipse(
            [(self.button_start_x - self.button_size//2, button_y - self.button_size//2),
             (self.button_start_x + self.button_size//2, button_y + self.button_size//2)],
            fill=self.button_red
        )
        
        # Yellow button (minimize)
        yellow_x = self.button_start_x + self.button_spacing
        draw.ellipse(
            [(yellow_x - self.button_size//2, button_y - self.button_size//2),
             (yellow_x + self.button_size//2, button_y + self.button_size//2)],
            fill=self.button_yellow
        )
        
        # Green button (maximize)
        green_x = self.button_start_x + (self.button_spacing * 2)
        draw.ellipse(
            [(green_x - self.button_size//2, button_y - self.button_size//2),
             (green_x + self.button_size//2, button_y + self.button_size//2)],
            fill=self.button_green
        )
        
        # Add title text
        try:
            # Try to use a system font
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        except:
            font = ImageFont.load_default()
        
        # Get text size
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Center the text in titlebar
        text_x = (terminal_width - text_width) // 2
        text_y = (self.titlebar_height - text_height) // 2
        
        draw.text((text_x, text_y), title, fill=self.text_color, font=font)
        
        # Paste terminal window onto background
        window_x = (new_width - terminal_width) // 2
        window_y = (new_height - terminal_height) // 2
        new_img.paste(terminal_window, (window_x, window_y), terminal_window)
        
        # Paste original screenshot into terminal window
        content_x = window_x + 1
        content_y = window_y + self.titlebar_height + 1
        new_img.paste(original, (content_x, content_y))
        
        # Save the result
        new_img.save(output_path, 'PNG')
        print(f"✅ Styled screenshot saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Add macOS terminal frame to screenshots')
    parser.add_argument('input', help='Input screenshot file')
    parser.add_argument('-o', '--output', help='Output file (default: adds _styled suffix)')
    parser.add_argument('-t', '--title', default='Terminal', help='Window title (default: Terminal)')
    
    args = parser.parse_args()
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        input_path = Path(args.input)
        output_path = input_path.parent / f"{input_path.stem}_styled{input_path.suffix}"
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Process the image
    styler = TerminalStyler()
    try:
        styler.add_terminal_frame(args.input, str(output_path), args.title)
    except Exception as e:
        print(f"❌ Error processing image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()