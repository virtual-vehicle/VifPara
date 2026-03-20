# StreamTracer

### *class* StreamTracer(vectors, seed_point_1=Vec(-5, -4, 0), seed_point_2=Vec(15, 4, 8), color_array_name=('POINTS', 'No color array'), representation_type='Surface', max_stream_length=20.0, resolution=1000, direction='BOTH')

Bases: `IViewObjectModifier`

Initialize a StreamTracer modifier used to visualize vector fields as streamlines.

The StreamTracer renders streamlines by integrating a vector field starting from
user-defined seed geometry. The resulting streamline geometry is rendered on top
of an existing 2D or 3D visualization.

* **Parameters:**
  * **vectors** ([*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple)) – The vector field used for streamline integration.
    Typically `('POINTS', <field_name>)`.
  * **seed_point_1** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – First point defining the line seed geometry.
  * **seed_point_2** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – Second point defining the line seed geometry.
  * **color_array_name** ([*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple)) – The array used to color the streamlines.
    Typically `('POINTS', <field_name>)`. Use `("POINTS", "No color array")` to
    disable scalar coloring and apply a uniform color.
  * **representation_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The representation used to display the streamlines.
    Common options include `"Wireframe"`, `"Surface"`, and `"3D Glyphs"`.
  * **max_stream_length** ([*float*](https://docs.python.org/3/library/functions.html#float)) – The maximum length of the generated streamlines.
  * **resolution** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The number of streamlines to render.
  * **direction** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The direction the streams should be spawned from the seed line.
    Can be `"BOTH"`, `"FORWARD"`, or `"BACKWARD"`.
  * **vectors**
  * **color_array_name**
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
