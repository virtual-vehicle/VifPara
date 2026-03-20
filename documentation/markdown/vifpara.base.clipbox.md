# Clipbox

### *class* Clipbox(case, position=Vec(-1, -2, 0), length=Vec(5, 4, 3))

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Create a Clipbox to cut a region from a loaded case.

The Clipbox allows to clip a case to focus on a certain aspect of it.
It takes a case and can then be used instead of the case when adding to a visualization 3d.

* **Parameters:**
  * **case** ([*Case*](vifpara.base.case.md#vifpara.base.case.Case)) – The loaded VifPara case to apply the clip to.
  * **position** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The clip box origin in x-, y-, and z-direction.
  * **length** ([*Vector3*](vifpara.other.vector3.md#vifpara.other.vector3.Vector3)) – The clip box size in x-, y-, and z-direction.
* **Returns:**
  None
