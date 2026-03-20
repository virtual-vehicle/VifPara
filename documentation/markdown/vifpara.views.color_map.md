# Color Map

### *class* ColorMap(field, legend_title=None, component_title='', legend_font='Times', title_font_size=16, label_font_size=16, legend_format_digits_before=6, legend_format_digits_after=2, legend_format_type='f', orientation='Horizontal', location='Lower Center', size=0.5, preset='Rainbow Desaturated', number_values=0, min_value=None, max_value=None, text_left='', text_right='', text_upper='', text_lower='', text_font_size=16, use_log_scale=False, field_type='POINTS')

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Initialize a ColorMap configuration used to define color mapping, color bar appearance,
legend formatting, and optional text annotations.

The ColorMap can be passed to the constructor of a slice to modify its value range and color representation.

* **Parameters:**
  * **field** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The field used for coloring. Also used as the legend title if no
    `legend_title` is provided.
  * **legend_title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The title to display above the color bar. If `None`,
    the `field` name is used.
  * **component_title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Optional component name appended to the legend title.
  * **legend_font** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Font used for the legend and annotation text. Options include:
    `'Arial'`, `'Courier'`, `'Times'`.
  * **title_font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Font size of the legend title.
  * **label_font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Font size of the labels along the color bar.
  * **legend_format_digits_before** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Number of digits before the decimal separator.
  * **legend_format_digits_after** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Number of digits after the decimal separator.
  * **legend_format_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Number format type:  
    - `'f'` → floating point  
    - `'e'` → exponential  
    - `'d'` → integer  
    - `'g'` → floating/exponential
  * **orientation** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Orientation of the color bar. Options:
    `'Horizontal'` or `'Vertical'`.
  * **location** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Screen placement of the color bar. Options include:
    `'Lower Center'`, `'Upper Center'`,  
    `'Lower Right Corner'`, `'Lower Left Corner'`,
    `'Upper Left Corner'`, `'Upper Right Corner'`.
  * **size** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Relative size of the color bar compared to the render view.
  * **preset** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Predefined ParaView color map preset (e.g., `'Viridis (matplotlib)'`,
    `'Turbo'`, `'Rainbow Desaturated'`).
  * **number_values** ([*int*](https://docs.python.org/3/library/functions.html#int)) – If > 0, the color map is discretized into this many values.
    If 0, a continuous color map is used.
  * **min_value** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Minimum scalar value for the color mapping.
  * **max_value** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Maximum scalar value for the color mapping.
  * **text_left** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Annotation on the left side of the render window.
  * **text_right** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Annotation on the right side.
  * **text_upper** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Annotation at the top.
  * **text_lower** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Annotation at the bottom.
  * **text_font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Font size for annotation text.
  * **use_log_scale** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether the color mapping should use a logarithmic scale.
  * **field_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Whether the coloring uses `"POINTS"` or `"CELLS"` data.
* **Returns:**
  None

#### apply_to_render_view(display, render_view, render=True)

Apply the color map and configure the color bar in the given render view.

This method:
- Applies the scalar coloring to the given display.
- Sets up the color transfer function (LUT).
- Applies preset colors, log scaling, min/max ranges, and discretization.
- Configures the scalar bar (legend) properties such as font, orientation, size, and label format.
- Shows or hides the color bar depending on the `render` flag.
- Optionally renders annotation text (left, right, upper, lower).

* **Parameters:**
  * **display** (*pv.Show*) – The geometry representation displayed in the render view.
  * **render_view** (*paraview.simple.RenderView*) – The render view in which the color bar is shown.
  * **render** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether the color bar should be visible. `True` = show, `False` = hide.
* **Returns:**
  None
