#!/bin/bash
# Initializes the documentation files. Completely removes all already existing documentation
# files and therefore all custom changes.
# ONLY use this if the documentation must be completely redone!!

USER_VALIDATION=""
while [[ $USER_VALIDATION != "y" && $USER_VALIDATION != "yes" && $USER_VALIDATION != "n" && $USER_VALIDATION != "no" ]]; do
    read -r -p "Do you really want to PURGE the full current documentation? This REMOVES ALL customizations (y/n): " USER_VALIDATION
done

if [[ $USER_VALIDATION == "n" || $USER_VALIDATION == "no" ]]; then
    echo "Exiting."
    exit 0
fi

echo ""
echo ""
echo "Reinitializing VifPara documentation"
echo "=============================================="
sleep 2.0

rm -rf docs
mkdir docs
cd docs
sphinx-quickstart
cd ..
sphinx-apidoc -o docs/ --separate --module-first src/vifpara