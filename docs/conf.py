
# docs/conf.py
import os
import sys
from datetime import datetime
from pathlib import Path
import tomllib


pyproject = tomllib.loads(Path("../pyproject.toml").read_text(encoding="utf-8"))
package_version = pyproject["project"]["version"]


def skip_undocumented_members(app, what, name, obj, skip, options):
    """Skip members without docstrings."""
    # If already marked to skip, respect that
    if skip:
        return True

    # Only skip functions, methods, and classes (not modules)
    if what in ("class", "function", "method"):
        doc = getattr(obj, "__doc__", None)
        if not doc or not doc.strip():
            return True  # skip if no docstring

    return False


def setup(app):
    app.connect("autodoc-skip-member", skip_undocumented_members)

# -- Path setup: make Sphinx find your package in src/  -----------------------
# Assumes project root: docs/ is next to src/
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# -- Project information -------------------------------------------------------
project = 'vifpara'
author = 'Virtual Vehicle Research GmbH'
copyright = f'{datetime.now():%Y}, {author}'
release = package_version

# -- General configuration -----------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',        # Import modules and extract docstrings
    'sphinx.ext.autosummary',    # Generate summary tables & stub pages
    'sphinx.ext.viewcode',       # Links to highlighted source
    'sphinx.ext.intersphinx',    # (optional) cross-link to external docs
    'sphinx.ext.doctest',        # (optional)
    'sphinx.ext.todo',           # (optional) todo directives
    'myst_parser',
    'sphinx_markdown_builder',
]

# If you use type hints, these options help render them nicely
autodoc_typehints = 'description'   # move type hints into description
autodoc_typehints_format = 'short'  # shorten 'module.Class' → 'Class'
autodoc_member_order = 'bysource'   # keep order as in source (or 'groupwise')
autoclass_content = 'both'          # or 'both' to include __init__ docstring
autosummary_generate = True         # autosummary pages are generated
add_module_names = False            # cleaner class/function names

# Read the Docs does not provide ParaView/VTK runtime dependencies.
# Mock these imports so autodoc can import modules and render docstrings.
autodoc_mock_imports = [
    'paraview',
    'paraview.simple',
    'paraview.web',
    'paraview.web.venv',
    'vtk',
]

# Intersphinx (optional): lets you link to external docs like Python, NumPy, etc.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

autodoc_default_options = {
    'exclude-members': 'utils'
}

autosummary_context = {
    'maxdepth': 1,
}

# -- HTML output ---------------------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']

# -- Misc options --------------------------------------------------------------
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
