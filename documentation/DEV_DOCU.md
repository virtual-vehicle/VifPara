# VifPara Developer Documentation

## Releasing
To release a new version, follow the next steps.

1. Write the new version number into the pyproject.toml (version = ). All other version occurences are automatically replaced with build.sh and generate_docs.sh.
2. Run the build.sh to build the new .whl file into the dist directory. This also automatically runs generate_docs.sh.
3. Add a comprehensive but brief update note to docs/UPDATES.md for your new version.

> **Warning**
> Each release MUST have a higher version number than the previous ones. Otherwise, the users could experience an unreliable installation process.

## Version Explanation
The version number must always follow the following pattern:

### <center><b>x.y.z</b></center>

x &rarr; Major changes/refactors, complete incompatibilities with previous versions.

y &rarr; Medium changes in the frameworks. Some workflows have been changed for the user.

z &rarr; Bugfixes and brief changes. Nothing significant has been changed for the user how to use the framwork.

The here used versioning is an adaption of GitFlow: https://gitversion.net/docs/learn/branching-strategies/gitflow/

## 📁 Project Structure

```
vifpara/
├── docs/                     # The documentation generation files
├── documentation/            # The rendered documentation files
├── examples/                 # Example testscase scripts
├── src/                      # Python packaging source files
├── test/                     # Scripts to quickly test the project
|
├── .readthedocs.yaml         # The configuration for the automatic documentation build
├── build.sh                  # Script for autobuilding package and setting up build venv
├── generate_docs.sh          # A script to render the documentation html files
├── initialize_docs.sh        # A script to freshly initialize all documentation generation files
├── LICENSE.txt               # The license of the project
├── pyproject.toml            # Python package build descriptor
├── README.md                 # The ReadMe entry point
├── requirements.txt          # The pip requirements for the project
└── test.sh                   # Tests all example scripts as intended
```

## Module Structure

- **`annotation`** - Annotation and labeling tools
- **`axes_grid`** - Grid and axes management
- **`case`** - Case loading and management for different file formats
- **`case_type`** - Enumeration of case types (OpenFOAM, Ensight, etc.)
- **`clipbox`** - Clipping and cropping functionality
- **`color_bar_view`** - Represents the view of a separate color bar for a slice.
- **`color_map`** - Color mapping and visualization settings
- **`config`** - Configuration management and file handling
- **`exporter`** - Handles all export of images and animations
- **`glyph`** - Glyph visualization (vectors, particles, etc.) to attach to a view
- **`layout`** - Layout management for all views
- **`plot_over_line`** - Line plots and data extraction
- **`pv_utils`** - Abstraction layer for bare paraview functions
- **`slice_matrix_color_type`** - Color type enumeration for slice matrices
- **`slice_matrix`** - Matrix of slices for comprehensive visualization
- **`slice`** - 2D slice creation and rendering
- **`text_view`** - Text view to render text in individual views
- **`vector3`** - 3D vector operations and utilities
- **`view_object_modifier`** - Base class for all view modifiers (e.g. glyphs)
- **`view_object`** - Base class for all views to embedd into a layout
- **`visualization_3D`** - 3D visualization and camera control