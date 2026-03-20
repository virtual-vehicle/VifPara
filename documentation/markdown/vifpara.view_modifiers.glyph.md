# Glyph

### *class* Glyph(orientation_array=('POINTS', 'No orientation array'), scale_array=('Points', 'No scale array'), scale_factor=0.0196, color=Vec(0, 0, 0), glyph_type='2D Glyph')

Bases: `IViewObjectModifier`

Initialize a Glyph modifier used to visualize vector fields as glyphs.

The Glyph allows to render glyphs (vector field directions) on top of a slice or 3d visualization.

* **Parameters:**
  * **orientation_array** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – The array defining glyph orientation.
    Typically `('POINTS', <field_name>)`.
  * **scale_array** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – The array defining glyph scaling.
    Typically `('POINTS', <field_name>)`.
  * **scale_factor** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The global scale factor applied when no scale array is used.
  * **color** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The diffuse color of the glyphs.
  * **glyph_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The glyph type determining the glyph geometry.
    Options include: `"2D Glyph"`, `"Arrow"`, `"Cone"`, `"Box"`,
    `"Cylinder"`, `"Line"`, `"Sphere"`.
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
