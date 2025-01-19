#!/bin/bash

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
export LDFLAGS=-L/opt/homebrew/lib
# check export or folder link
brew install weasyprint pyside qt
python3 -m pip install -r requirements.txt