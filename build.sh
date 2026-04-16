#!/bin/bash
# Activates the build venv and performs the following steps in this order:
# - builds the wheel file
# - regenerates user documentation
# - updates version numbering in README.md

# Extract version from pyproject.toml
version="$(
  awk '
    $0 ~ /^\[project\]/ { in_project=1; next }
    in_project && $0 ~ /^\[/ { in_project=0 }
    in_project && $0 ~ /^version[[:space:]]*=/ {
      if (match($0, /"[^"]+"/)) {
        print substr($0, RSTART + 1, RLENGTH - 2)
        exit
      }
    }
  ' pyproject.toml
)"

echo "===================================================="
echo "Building VifPara version ${version}."
echo "===================================================="
sleep 3.0

# Load environment and install requirements
if [[ ! -d venv ]]; then
  python3 -m venv --system-site-packages venv
fi
source venv/bin/activate
python3 -m pip install --upgrade build
pip install -r requirements.txt

# Build wheel file
echo ""
echo ""
echo "Building VifPara wheel file (python package)"
echo "=============================================="
sleep 2.0

find dist/ -name '*.whl' -delete
find dist/ -name '*.tar.gz' -delete
python3 -m build

# Generates the updated documentation.
echo ""
echo ""
echo "Generating VifPara documentation"
echo "=============================================="
sleep 2.0

./generate_docs.sh

# Sync README version badge with the package version from pyproject.toml.
echo ""
echo ""
echo "Updating version number in README.md"
echo "=============================================="
sleep 2.0

if [[ -z "$version" ]]; then
  echo "Error: Could not read [project].version from pyproject.toml" >&2
  exit 1
fi

if ! grep -q '<img alt="Version" src=https://img.shields.io/badge/Version-' README.md; then
  echo "Error: Version badge not found in README.md" >&2
  exit 1
fi

export VIFPARA_VERSION="$version"
perl -0777 -i -pe 's#(<img alt="Version" src=https://img\.shields\.io/badge/Version-).*?(-green\?style=flat-square>)#$1$ENV{VIFPARA_VERSION}$2#g' README.md

if ! grep -q "Version-${version}-green?style=flat-square" README.md; then
  echo "Error: Failed to update README.md version badge" >&2
  exit 1
else
  echo "Updated version number in README.md."
fi
