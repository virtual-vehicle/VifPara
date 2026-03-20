# Annotation

### annotate_time(view_object, font='Times', font_size=19, window_location='Upper Left Corner', digits_after_comma=2, unit='s')

Add a time annotation overlay to a view.

* **Parameters:**
  * **view_object** (*IViewObject*) – The view object to annotate with the current simulation time.
  * **font** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Font used for the annotation (e.g., `"Times"`, `"Arial"`, `"Courier"`).
  * **font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Font size of the displayed time label.
  * **window_location** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The location of the time annotation within the view.
    Options include: `"Upper Left Corner"`, `"Upper Right Corner"`,
    `"Upper Center"`, `"Lower Left Corner"`, `"Lower Center"`, `"Lower Right Corner"`.
  * **digits_after_comma** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Number of decimal places to display.
    If `0`, the time is shown as an integer.
  * **unit** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The time unit appended to the label (e.g., `"s"`, `"ms"`, `"h"`).
* **Returns:**
  None

### annotate_coordinates(view_object, vector, font='Times', font_size=19, window_location='Upper Center', digits_after_comma=3)

Add a coordinate annotation (X, Y, Z) to a view.

* **Parameters:**
  * **view_object** (*IViewObject*) – The view object to annotate.
  * **vector** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3) *|*[*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *|*[*list*](https://docs.python.org/3/library/stdtypes.html#list)) – The coordinate triple to annotate. May be a `Vector3` or 
    a tuple/list of floats.
  * **font** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Font used for the annotation text.
  * **font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Size of the annotation text.
  * **window_location** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Placement of the annotation inside the render view.
  * **digits_after_comma** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Number of decimal places for formatting the coordinate values.
* **Returns:**
  None

### annotate_text(view_object, text, font='Times', font_size=19, window_location='Upper Center')

Add an arbitrary text annotation to a view.

* **Parameters:**
  * **view_object** (*IViewObject*) – The view object to annotate.
  * **text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The text content to display.
  * **font** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Font used for the annotation text.
  * **font_size** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Size of the annotation text.
  * **window_location** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Placement of the annotation inside the render view.
* **Returns:**
  None
