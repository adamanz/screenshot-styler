#!/bin/bash

# Screenshot Styler - Fast wrapper script
# Handles virtual environment and dependencies automatically

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/terminal_styler.py"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Setting up virtual environment..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install -q Pillow
else
    source "$VENV_DIR/bin/activate"
fi

# Run the Python script with all arguments
python "$PYTHON_SCRIPT" "$@"