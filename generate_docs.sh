#!/bin/bash
# Generates all documentation files.

sphinx-build -b html docs documentation/html
sphinx-build -b markdown docs documentation/markdown