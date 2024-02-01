#!/bin/bash

# Installing dependencies using pip3
pip3 install -r requirements.txt

# SQLite3 Installation
# Checks if SQLite3 is already installed
if ! command -v sqlite3 &> /dev/null; then
    # Install SQLite3 if not already installed
    sudo apt update
    sudo apt install sqlite3
fi
# Allows Python script execution
chmod +x gxsuid.py
echo "Installation complete."
