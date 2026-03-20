# Vector3

### *class* Vector3(x, y, z)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Initialize a 3-dimensional vector.

* **Parameters:**
  * **x** ([*float*](https://docs.python.org/3/library/functions.html#float) *|*[*int*](https://docs.python.org/3/library/functions.html#int)) – The x-component of the vector.
  * **y** ([*float*](https://docs.python.org/3/library/functions.html#float) *|*[*int*](https://docs.python.org/3/library/functions.html#int)) – The y-component of the vector.
  * **z** ([*float*](https://docs.python.org/3/library/functions.html#float) *|*[*int*](https://docs.python.org/3/library/functions.html#int)) – The z-component of the vector.
* **Returns:**
  None

#### *classmethod* from_list(vector)

Create a `Vector3` instance from a list of numerical values.

* **Parameters:**
  **vector** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *|*[*int*](https://docs.python.org/3/library/functions.html#int) *]*) – A list containing three numeric components `[x, y, z]`.
* **Return Vector3:**
  A new `Vector3` constructed from the list values.

#### *classmethod* right()

Create a right-direction unit vector `(1.0, 0.0, 0.0)`.

* **Return Vector3:**
  A unit vector pointing in the positive X direction.

#### *classmethod* up()

Create an up-direction unit vector `(0.0, 1.0, 0.0)`.

* **Return Vector3:**
  A unit vector pointing in the positive Y direction.

#### *classmethod* forward()

Create a forward-direction unit vector `(0.0, 0.0, 1.0)`.

* **Return Vector3:**
  A unit vector pointing in the positive Z direction.

#### *classmethod* zero()

Create a zero vector `(0.0, 0.0, 0.0)`.

* **Return Vector3:**
  A vector with all components set to zero.

#### *classmethod* one()

Create a ones vector `(1.0, 1.0, 1.0)`.

* **Return Vector3:**
  A vector with all components set to one.

#### set(x, y, z)

Set all three components of the vector.

* **Parameters:**
  * **x** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The new x-component value.
  * **y** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The new y-component value.
  * **z** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The new z-component value.
* **Returns:**
  None
* **Return type:**
  None

#### dot(rhs)

Compute the dot product between this vector and another.

* **Parameters:**
  **rhs** ([*Vector3*](#vifpara.other.vector3.Vector3)) – The vector to compute the dot product with.
* **Return float|int:**
  The resulting dot product value.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If `rhs` is not a `Vector3`.

#### cross(rhs)

Compute the cross product between this vector and another.

* **Parameters:**
  **rhs** ([*Vector3*](#vifpara.other.vector3.Vector3)) – The vector to compute the cross product with.
* **Return Vector3:**
  A new vector representing the cross product result.
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If `rhs` is not a `Vector3`.

#### magnitude()

Compute the magnitude (Euclidean length) of the vector.

* **Return float:**
  The computed vector magnitude.

#### normalized()

Return a normalized (unit‑length) version of this vector.

If the vector has zero magnitude, the result is `Vector3(0, 0, 0)`.

* **Return Vector3:**
  The normalized vector.

#### to_list()

Convert the vector into a Python list.

* **Return list[int|float]:**
  A list containing `[x, y, z]`.
