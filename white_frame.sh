#!/bin/bash

# Simple White Frame Styler - Fast wrapper script
# Handles virtual environment and dependencies automatically

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/simple_frame_styler.py"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Setting up virtual environment..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -q Pillow
else
    source "$VENV_DIR/bin/activate"
fi

# Run the Python script and capture output
OUTPUT=$(python "$PYTHON_SCRIPT" "$@" 2>&1)
echo "$OUTPUT"

# Extract the output path from the success message
OUTPUT_PATH=$(echo "$OUTPUT" | grep -o '/[^"]*_framed\.png')

# If output path was found, open it
if [ -n "$OUTPUT_PATH" ]; then
    echo "🖼️  Opening framed screenshot..."
    open "$OUTPUT_PATH"
fi