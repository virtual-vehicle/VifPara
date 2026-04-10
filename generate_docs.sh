#!/bin/bash
# Generates all documentation files.

source venv/bin/activate
sphinx-build -b html docs documentation/html
sphinx-build -b markdown docs documentation/markdown
