# Axes Grid

### *class* AxesGrid(x_title='X Axis', y_title='Y Axis', z_title='Z Axis', title_font_size=20, font='Times', label_font_size=16)

Bases: `IViewObjectModifier`

Initialize an AxesGrid modifier used to visualize a 3‑axis coordinate grid.

The axes AxesGrid can be used to visualize the axes of a 3d visualization,
or a slice. It can be attached to a view.

This modifier configures axis titles, fonts, and label sizes for the ParaView
axes grid displayed in a render view.

* **Parameters:**
  * **x_title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The title of the x‑axis.
  * **y_title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The title of the y‑axis.
  * **z_title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The title of the z‑axis.
  * **title_font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Font size for the axis titles.
  * **font** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Font family used for axis titles. Options include:
    `"Arial"`, `"Courier"`, `"Times"`.
  * **label_font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Font size for the numeric axis labels.
* **Returns:**
  None

#### attach(view_object)

Attach this modifier to the given view object.

This method registers the modifier’s `render_callback` with the
provided view object. When the view renders, the callback will be
invoked, allowing the modifier to alter or extend the rendering
process.

* **Parameters:**
  **view_object** (*IViewObject*) – The view object to which the modifier
  should be attached.
* **Returns:**
  None
