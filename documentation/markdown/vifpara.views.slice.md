# Slice

### *class* Slice(, case, origin=Vec(0, 0, 1), normal=Vec(1, 0, 0), camera_up=Vec(0, 0, 1), slice_type='Plane', height=135, color_map=None, margin_x=0, margin_y=0, offset_x=0, offset_y=0, zoom=1.0, show_orientation_axis=False, representation_type='Surface', representation_point_size=1.0)

Bases: `IViewObject`

Initialize a Slice object used to extract and visualize a planar slice
from a loaded dataset.

The Slice represents a 2 dimensional rendered plane through a case.
It can be used to see “inside” a case. It can be zoomed, offset, etc.

* **Parameters:**
  * **case** ([*Case*](vifpara.base.case.md#vifpara.base.case.Case)) – The loaded VifPara case.
  * **origin** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The origin point of the slice plane.
  * **normal** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The normal vector defining the slice plane direction.
  * **camera_up** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The camera’s up-vector inside the slice view.
  * **slice_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The type of slice (e.g., `"Plane"`).
  * **height** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The height of the screenshot in pixels.
  * **color_map** ([*ColorMap*](vifpara.views.color_map.md#vifpara.views.color_map.ColorMap)) – The color mapping configuration. If `None`,
    the slice is displayed with a default gray color.
  * **margin_x** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Optional horizontal margin (positive = wider image,
    negative = tighter crop).
  * **margin_y** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Optional vertical margin (positive = taller image,
    negative = tighter crop).
  * **offset_x** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Horizontal camera shift. Positive moves the camera right,
    negative left.
  * **offset_y** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Vertical camera shift. Positive moves the camera down,
    negative up.
  * **zoom** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Zoom factor for the 3D visualization (2.0 = 2× larger,
    0.5 = half size).
  * **show_orientation_axis** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to show the orientation axis widget.
  * **representation_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The data representation type (`"Surface"` or `"Points"`).
  * **representation_point_size** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Point size when using point-based representations.
* **Returns:**
  None

#### *static* generate_slice_array(case, generator_direction, num_slices, \*\*kwargs)

Generate an array of Slice objects placed along a direction vector.

This static method automatically computes a sequence of slice origins along the
bounding box of the given case. It is useful for exploring datasets by quickly
generating multiple evenly spaced slices through the domain.

Any keyword arguments valid for the Slice constructor may be passed, except
`origin` which is ignored because origins are auto‑generated.  
If `normal` is not provided, the `generator_direction` is used as the slice normal.

* **Parameters:**
  * **case** ([*Case*](vifpara.base.case.md#vifpara.base.case.Case)) – The case in which slices will be generated.
  * **generator_direction** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The direction along which the slices are placed.  
    If no `normal` is provided via kwargs, this vector will be used.
  * **num_slices** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The number of slices to generate. Higher values lead to
    finer spacing along the generator direction.
  * **kwargs** – Additional keyword arguments forwarded to the Slice constructor
    (e.g., `color_map=cmap`, `camera_up=Vector3.forward()`).  
    The keyword `origin` is not allowed and will be ignored.
* **Return List[Slice]:**
  A list containing all generated Slice instances.
* **Return type:**
  [*List*](https://docs.python.org/3/library/typing.html#typing.List)[[*Slice*](#vifpara.views.slice.Slice)]

#### set_color_bar_size(height=None, width=None)

Set the size of the color bar view for the slice.

If no value is provided:
- `height` defaults to `80` pixels.
- `width` defaults to the width of the slice view.

* **Parameters:**
  * **height** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The height of the color bar in pixels. If `None`, the default
    height of `80` px is used.
  * **width** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The width of the color bar in pixels. If `None`, the width of
    the slice view is used.
* **Returns:**
  None

#### render_color_bar(layout, row=0, col=0)

Render the slice’s color bar into a specific cell of the layout.

* **Parameters:**
  * **layout** ([*Layout*](vifpara.base.layout.md#vifpara.base.layout.Layout)) – The layout into which the color bar should be rendered.
  * **row** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The target row index in the layout.
  * **col** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The target column index within the selected row.
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
