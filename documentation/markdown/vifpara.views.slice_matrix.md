# Slice Matrix

### *class* SliceMatrix(slices, texts_top=None, texts_left=None, color_type=SliceMatrixColorType.COLOR_CENTERED, height_slice=520, width_text=300, height_color_bar=150, font=None, font_size=None, text_view_height=100)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Initialize a SliceMatrix, a structured arrangement of slices with optional
text annotations and color bar configurations.

A SliceMatrix can be used to render multiple slices at once into a layout.
It can additionally render color bars, and descriptive text.

A SliceMatrix reserves the entire layout and manages its own internal structure.
No additional views can be added once the layout is dedicated to a slice matrix.

* **Parameters:**
  * **slices** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*Slice*](vifpara.views.slice.md#vifpara.views.slice.Slice) *]*) – The list of Slice objects that will be rendered.
  * **texts_top** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Text annotations for the top row (one per column).
  * **texts_left** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Text annotations for the left column (one per row).
  * **color_type** ([*SliceMatrixColorType*](vifpara.views.slice_matrix_color_type.md#vifpara.views.slice_matrix_color_type.SliceMatrixColorType)) – Defines the color bar strategy for the matrix.
  * **height_slice** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Height in pixels of each slice in the matrix.
  * **width_text** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Width in pixels of the left‑side text views (if any).
  * **height_color_bar** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Height in pixels of the color bars in the matrix.
  * **font** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Font used for text annotations (e.g., `"Times"`, `"Courier"`, `"Arial"`).
  * **font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Font size used for text annotations.
  * **text_view_height** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Height in pixels of the top text views.
* **Returns:**
  None

#### render(layout)

Render the slice matrix into the provided layout.

This method organizes and renders:
- The slice grid
- Optional top text row
- Optional left text column
- Color bars (depending on the slice matrix color mode)

The layout is modified by inserting additional rows and/or columns
to accommodate text annotations and color bars as required by the
chosen SliceMatrixColorType.

* **Parameters:**
  **layout** ([*Layout*](vifpara.base.layout.md#vifpara.base.layout.Layout)) – The layout into which the slice matrix should be rendered.
* **Returns:**
  None
