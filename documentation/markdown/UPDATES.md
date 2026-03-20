# Update Log

<b>1.3.3</b> | 2026-03-17

- Implemented basic single file loading into cases by using the “file” loader argument in the Case constructor.

<b>1.3.2</b> | 2026-03-11

- Completely overhauled documentation.
- Fixed Windows issues with capturing stderror with the logger.

<b>1.3.1</b> | 2025-12-15

- Hotfix: Binned NumPy version to match ParaView NumPy versions.

<b>1.3.0</b> | 2025-12-09

- Completely overhauled installation and run methods. Please consult the installation documentation for changes.
- Using the vifpara runner command now always enables headless rendering. No need for the xvfb-run hack anymore.
- Cell and point arrays can now be logged and selected in the loaded case.
- First prototype of multiblock support. Multiblock names can now be logged and selected in the loaded case. Needs more testing.
- Color maps can now represent either a cell or a point array via a new parameter.
- Fixed a bug that led to errors in computations between integers and floats in Vector3.
- Slices in Visualization3D can now be scaled up or down.
- Color maps in Visualization3D can now be hidden.
- Passing None as a color map for a view now results in a solid grey coloring.
- Time annotation now allows configurable units.

<b>1.2.1</b> | 2025-11-12

- Plot-over-line view is now available, allowing the rendering of line charts of scalar fields along a defined line in the case. It can also export its line chart data as a CSV file at every timestep in the case.
- The obsolete MeshFree directory has been removed to avoid confusion due to inconsistent user documentation.
- Fixed a mathematical inconsistency when rendering slices with a modified camera-up vector, which led to reduced view sizes or even empty views.
- Fixed a bug in the config that forced users to provide a logs directory.
- Fixed decimal point display in color bars, even when the decimal count was set to 0.
- Clarified parts of the installation instructions.

<b>1.2.0</b> | 2025-10-10

- REFACTOR: Layout is no longer passed to the ViewObject constructor, but to the render() method. This allows for more dynamic use and future development.
- Implemented a slice generation method that automatically slices a case into n slices through the center of the case (Slice.generate_slice_array()).
- Fixed a bug where zero width/height views or layouts caused program crashes.
- Added a method to the Case class to fetch the data range of a scalar field.
- Attempted to automatically rescale color maps to the data range when no min/max was provided.
- Color maps can now be set to logarithmic scale.
- Frame windows can now be selected for animation export.
- Renamed some export methods to clarify their usage.
- Removed redundant export methods and cleaned up the remaining ones.
- Users can now show the orientation axis in views.

<b>1.1.1</b> | 2025-10-02

- Removed the ability to pass a rendering view to a view object.
- From now on, the workflow always lets the view object constructor generate the rendering view, which can then be modified later.

<b>1.1.0</b> | 2025-10-02

- Refactored the internal project structure. It is now more maintainable, and new developers can get into the framework more easily.
- The structure now consists of different modules, mainly base, views, and view modifiers. Most elements of VifPara now belong to one of these three categories.
- View modifier attachment now happens by registering the modifier to the view and only calling its rendering routines when the view’s render method is executed. This allows for better rendering control, framework unification, and improved maintainability.
- Reworked the axes grid class into a view modifier.
- Glyph types can now be selected, and glyphs are 2D arrows by default.

<b>1.0.3</b> | 2025-09-30

- Fixed several small Python syntax issues that could lead to exceptions on certain Python versions.

<b>1.0.2</b> | 2025-09-30

- Removed standard error routing on Windows, which previously led to exceptions.

<b>1.0.1</b> | 2025-09-30

- Added colorization of logging output.

<b>1.0.0</b> | 2025-09-29

- Complete overhaul of layouts and views.
- Adapted the framework to better handle multi-view rendering.
- Added more settings for views. Zooming, panning, etc. are now possible inside a view.
- Slice matrices are now smart and do not require users to think about additional rows or columns for text and color bars.
- Significantly simplified the workflow with VifPara.
- Config is now a class responsible for loading, storing, and providing directory and case data.

<b>0.1.3</b> | 2025-09-03

- Scripts started on Windows no longer require importing the ParaView virtual environment (import paraview.web.venv).
- Fixed a bug in the Windows script launching process where the first Python argument was ignored.

<b>0.1.2</b> | 2025-07-31

- Updated the setup and release system. Users can now download ZIP files for Linux and Windows releases.

<b>0.1.1</b> | 2025-07-30

- First release of the Python package structure.
