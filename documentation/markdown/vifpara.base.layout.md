# Layout

### *class* ScaleIdEntry(scale_id: [int](https://docs.python.org/3/library/functions.html#int), inv_fraction: [bool](https://docs.python.org/3/library/functions.html#bool))

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

* **Parameters:**
  * **scale_id** ([*int*](https://docs.python.org/3/library/functions.html#int))
  * **inv_fraction** ([*bool*](https://docs.python.org/3/library/functions.html#bool))

#### scale_id *: [int](https://docs.python.org/3/library/functions.html#int)* *= -1*

#### inv_fraction *: [bool](https://docs.python.org/3/library/functions.html#bool)* *= False*

### *class* Layout(cell_array)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Initialize a layout used as the basis for image and animation exports.

The layout is the basic building block for visualization.
Use it to render one or multiple views or a slice matrix.
Then you can pass the layout to an exporter to export it as images or animations.

A layout consists of rows and columns of view cells. Each cell will contain
one rendered view. All cells must be assigned a view before exporting,
otherwise the export will fail.

Example:
: A `cell_array` like `[3, 2, 4]` creates a layout with three rows:
  - Row 1 contains 3 cells
  - Row 2 contains 2 cells
  - Row 3 contains 4 cells

* **Parameters:**
  **cell_array** ([*list*](https://docs.python.org/3/library/stdtypes.html#list)) – A descriptor defining the number of columns (cells)
  in each row of the layout.
* **Returns:**
  None

#### delete_layout()

Delete the current layout from ParaView.

This removes the internal ParaView layout object and marks it as unusable.
After this call, the layout should no longer be used.

* **Returns:**
  None

#### set_height(height)

Set the height of the layout, which determines the resolution of exported images or animations.

The width is automatically computed based on this height.  
This is required because ParaView can break the layout configuration when exporting images
larger than the physical screen size, so controlling the resolution avoids this issue.

* **Parameters:**
  **height** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The height of the exported image in pixels.
* **Returns:**
  None
