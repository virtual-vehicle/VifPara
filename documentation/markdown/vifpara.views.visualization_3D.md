# Visualization 3D

### *class* Visualization3D(case, cam_position, cam_up=Vec(0, 0, 1), focal_point=Vec(0, 0, 0), width=900, height=720, zoom=1.0, show_orientation_axis=False, show_color_bar=True)

Bases: `IViewObject`

Initialize a 3D visualization view for displaying slice planes and geometry.

The 3D visualization renders the case or clipbox as is into a layout cell.
Slices can additionally be added to render their position on the case.
This allows for an “overview” of your the slices you defined.

* **Parameters:**
  * **case** ([*Case*](vifpara.base.case.md#vifpara.base.case.Case)) – The loaded visualization case.
  * **cam_position** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The world‑space position of the camera.
  * **cam_up** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The camera’s up vector. Defaults to `(0, 0, 1)`.
  * **focal_point** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The point the camera looks at. Defaults to `(0, 0, 0)`.
  * **width** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The width of the 3D render view in pixels.
  * **height** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The height of the 3D render view in pixels.
  * **zoom** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Zoom factor for the camera.  
    `2.0` → twice the size, `0.5` → half the size.
  * **show_orientation_axis** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to show the ParaView orientation axis.
  * **show_color_bar** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to show a color bar in the 3D view.
* **Returns:**
  None

#### add_case_or_clip_to_view(case, color_map=None, opacity=1.0, representation_type='Surface', gaussian_radius=0.0012, field_type='Points', representation_point_size=1.0)

Add a Case or Clipbox object to the 3D visualization.

This function:
- Shows the case or clip object in the 3D render view.
- Applies an optional color map.
- Sets the representation, opacity, point size, and additional rendering options.
- Supports both point-based and cell-based field data.
- Can render Gaussian-point representations when using `'Point Gaussian'`.

* **Parameters:**
  * **case** ([*Case*](vifpara.base.case.md#vifpara.base.case.Case)) – The Case or Clipbox instance to visualize.
  * **color_map** ([*ColorMap*](vifpara.views.color_map.md#vifpara.views.color_map.ColorMap)) – The color map applied to the object. If `None`, the object is shown in gray.
  * **opacity** ([*float*](https://docs.python.org/3/library/functions.html#float)) – The opacity of the displayed object (0.0–1.0).
  * **representation_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The data representation (e.g. `"Surface"`, `"Points"`,
    `"Point Gaussian"`).
  * **gaussian_radius** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Radius used for Gaussian point rendering (only relevant for
    `"Point Gaussian"` representation).
  * **field_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Field data type. Set to `"Cells"` for cell-only datasets, otherwise `"Points"`.
  * **representation_point_size** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Size of points when using point-based representations.
* **Returns:**
  None

#### add_slice_to_view(slice, text='', opacity=0.4, text_position=None, flip_y_label=False, text_scale=0.05, slice_scale=1.0)

Add a slice plane and optional text annotation to the 3D view.

This method:
- Positions a slice plane in the 3D view according to its geometric definition.
- Applies opacity and scaling.
- Optionally adds a 3D text label aligned with slice orientation and camera direction.
- Automatically computes transform, rotation, and placement of text.

* **Parameters:**
  * **slice** ([*Slice*](vifpara.views.slice.md#vifpara.views.slice.Slice)) – The slice whose geometric plane should be added to the 3D view.
  * **text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Optional annotation text displayed near the slice. If empty, no text is shown.
  * **opacity** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Opacity of the slice plane (0.0–1.0).
  * **text_position** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *|*[*list*](https://docs.python.org/3/library/stdtypes.html#list) *|**None*) – Optional 3‑component position where the text should appear.
  * **flip_y_label** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether the text’s y‑orientation should be flipped. Useful when the camera’s
    up‑vector is aligned along the y‑axis.
  * **text_scale** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Scale factor for the 3D text annotation.
  * **slice_scale** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Scaling factor applied to the slice plane geometry.
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
