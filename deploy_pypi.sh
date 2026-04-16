#!/bin/bash
# Deploys the Python wheel package to the PyPi repository.
# Requires API keys in order to work.

twine upload dist/*
