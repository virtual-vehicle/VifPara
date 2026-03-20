# Plot Over Line

### *class* PlotOverLine(case, start_point, end_point, fields, height=135)

Bases: `IViewObject`

Initialize a PlotOverLine view for sampling scalar fields along a line and rendering
an XY chart representation.

The PlotOverLine view element, can be used to render a line chart, which represents a
scalar field over a certain, defined line inside your case.
You can then show this chart in a cell of your layout.
It also has the additional capability to export its data in a csv file.

This class enables:
: - Sampling multiple scalar fields along a line in 3D space.
  - Rendering the sampled data in a ParaView XY chart.
  - Exporting the underlying sampled values as CSV.

* **Parameters:**
  * **case** ([*Case*](vifpara.base.case.md#vifpara.base.case.Case)) – The case from which field data is extracted.
  * **start_point** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The start point of the sampling line.
  * **end_point** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The end point of the sampling line.
  * **fields** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – The scalar field names to extract and plot.
  * **height** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The height of the view representation inside the layout.
* **Returns:**
  None

#### get_render_object()

Get the underlying ParaView PlotOverLine object.

* **Returns:**
  The internal PlotOverLine filter used for sampling along the line.
* **Return type:**
  pv.PlotOverLine

#### export_as_csv(config, filename, timestep=0.0, show_timestep=True)

Export the sampled scalar field data along the line to a CSV file.

The output is written into the plots directory defined by the provided `Config` object.
The underlying pipeline is re‑evaluated at the specified timestep before export.

* **Parameters:**
  * **config** ([*Config*](vifpara.base.config.md#vifpara.base.config.Config)) – The configuration object providing the output directory.
  * **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The output filename without the `.csv` extension.
  * **timestep** ([*float*](https://docs.python.org/3/library/functions.html#float)) – The timestep from which data should be sampled.
  * **show_timestep** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True`, additional columns with the timestep
    information are added to the exported CSV.
* **Returns:**
  None

#### delete_view()

Delete the underlying render view.

This method removes the associated ParaView render view from the
visualization pipeline and logs that the view should no longer be used.

* **Returns:**
  None

#### get_case()

Return the loaded case this view is based on.

* **Returns:**
  The loaded case of the view object.
* **Return type:**
  [Case](vifpara.base.case.md#vifpara.base.case.Case)

#### get_height()

Return the height of the view in pixels.

If the internally stored height is less than or equal to zero, a warning
is logged and the height is set to a failsafe value of `10` to prevent
division-by-zero issues during rendering.

* **Returns:**
  The height of the view in pixels.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### get_render_view()

Return the underlying ParaView render view.

This method provides access to the internal `_render_view` attribute,
which represents the ParaView `RenderView` used by the view for
visualization.

* **Returns:**
  The associated ParaView render view.

#### get_width()

Return the width of the view in pixels.

If the internally stored width is less than or equal to zero, a warning
is logged and the width is set to a failsafe value of `10` to prevent
division-by-zero issues during rendering.

* **Returns:**
  The width of the view in pixels.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### render(layout, row=0, col=0)

Render the view into the given layout and apply modifiers.

This method performs the following steps in order:
1. Validates that `layout` is a `Layout` instance.
2. Renders the view’s own content via `_render_inside` at the specified grid
position (`row`, `col`).
3. Toggles the orientation axes visibility on the underlying render view,
if available.
4. Applies all attached render modifiers via `_render_modifiers`.
5. If both a display and block selectors are present, applies the block selection
to the display.

* **Parameters:**
  * **layout** ([*Layout*](vifpara.base.layout.md#vifpara.base.layout.Layout)) – The layout grid where the view should be placed.
  * **row** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Target row index in the layout grid. Defaults to `0`.
  * **col** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Target column index in the layout grid. Defaults to `0`.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If `layout` is not an instance of `Layout`.
* **Returns:**
  None

#### set_blocks(blocks)

Set the list of blocks to be displayed in the view.

This method assigns the provided list of block identifiers to the internal
`_blocks` attribute, determining which blocks are shown in the rendered
output.

* **Parameters:**
  **blocks** (*List* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – A list of block names or identifiers.
* **Returns:**
  None
