# Terminal Screenshot Styler

Automatically add a beautiful macOS-style terminal window frame to your screenshots.

## Features

- Adds macOS-style window frame with traffic light buttons
- Dark theme styling matching modern terminal aesthetics
- Customizable window title
- Preserves original screenshot quality

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage
python terminal_styler.py screenshot.png

# With custom output file
python terminal_styler.py screenshot.png -o styled_screenshot.png

# With custom window title
python terminal_styler.py screenshot.png -t "Claude Code Token Usage Report - Daily"
```

## Examples

The script transforms plain screenshots into terminal-styled images with:
- Dark background with padding
- Terminal window with rounded corners
- macOS traffic light buttons (red, yellow, green)
- Customizable title bar text

## Requirements

- Python 3.6+
- Pillow (PIL)

## License

MIT