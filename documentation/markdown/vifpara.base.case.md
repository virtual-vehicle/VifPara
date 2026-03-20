# Case

### *class* Case(, config, loader='openfoam', case_type=CaseType.RECONSTRUCTED)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Initialize a new case and load it using the specified ParaView reader.

The case is the central object everything revolves around. Create it by passing
a config instance with the correct case path. Then you can set the loader to load OpenFoam or MeshFree cases.

* **Parameters:**
  * **config** ([*Config*](vifpara.base.config.md#vifpara.base.config.Config)) – The preloaded configuration object providing the case path.
  * **loader** (*LoaderType*) – The reader type to use. Can be “openfoam”, “ensight”, or “file”. Capitalization does
    not matter. The “file” specifier allows to read arbitrary file types, such as stl, vtu, pvd
  * **case_type** ([*CaseType*](vifpara.base.case_type.md#vifpara.base.case_type.CaseType)) – The type of case to load (e.g., reconstructed).
* **Returns:**
  None
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If the loader is incompatible with the case type.

#### get_blocknames()

Get all multiblock names from the case.
:return List[str]: A list containing the hierarchical names of all blocks in the dataset’s VTK data assembly.

#### log_blocknames()

Log all multiblock names available in the case.

This prints a formatted list of all block names to the application logger.

* **Returns:**
  None

#### get_case()

Get the underlying ParaView case object.

* **Returns:**
  The internal ParaView data source representing the loaded case.

#### set_mesh_regions(mesh_regions)

Set the mesh regions that determine which parts of the case are rendered.

* **Parameters:**
  **mesh_regions** (*List* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – A list of region names to be rendered.Common default is `["internalMesh"]`.
* **Returns:**
  None

#### get_range(field_name, force_update=False)

Get the minimum and maximum values of a scalar field in the loaded case.

This method searches first in point data and then in cell data.  
If the field does not exist, `None` is returned.  
On the first call, or when `force_update` is `True`, the pipeline is updated
which may take additional time.

* **Parameters:**
  * **field_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The name of the scalar field whose value range should be extracted.
  * **force_update** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True`, forces a pipeline update before reading the field range.
* **Return Optional[Tuple[float, float]]:**
  A `(min, max)` tuple representing the field range, or `None` if the field is not found.
* **Return type:**
  [*Tuple*](https://docs.python.org/3/library/typing.html#typing.Tuple)[[float](https://docs.python.org/3/library/functions.html#float), [float](https://docs.python.org/3/library/functions.html#float)] | None

#### set_point_arrays(point_arrays)

Set the active point arrays for the case.

* **Parameters:**
  **point_arrays** (*List* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – A list of point array names to enable on the data source.
* **Returns:**
  None

#### set_cell_arrays(cell_arrays)

Set the active cell arrays for the case.

* **Parameters:**
  **cell_arrays** (*List* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – A list of cell array names to enable on the data source.
* **Returns:**
  None

#### get_time_step_count()

Get the number of available time steps in the loaded case.

* **Return int:**
  The total number of time steps.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

#### log_patch_array_info()

Log all available mesh regions and their current selection status.

The output lists each mesh region along with its activation flag
and is written to the application logger.

* **Returns:**
  None

#### log_cell_arrays()

Log all available cell arrays.

This prints a formatted list of cell array names to the application logger,
allowing the user to inspect which fields are available for cell‑based operations.

* **Returns:**
  None

#### log_point_arrays()

Log all available point arrays.

This prints a formatted list of point array names to the application logger,
allowing inspection of which point-based fields are available.

* **Returns:**
  None

#### get_point_arrays()

Get the list of available point arrays from the case.

* **Return List[str]:**
  A list of point array names provided by the data source.
* **Return type:**
  [*List*](https://docs.python.org/3/library/typing.html#typing.List)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

#### get_patch_array_info()

Get all available mesh regions and their activation status.

Each entry contains:
- `name` (str): The mesh region name.
- `status` (int): `1` if selected, `0` if not selected.

* **Return List[dict]:**
  A structured list containing information about all mesh regions and whether each region is currently active.
* **Return type:**
  [*List*](https://docs.python.org/3/library/typing.html#typing.List)[[dict](https://docs.python.org/3/library/stdtypes.html#dict)]

#### get_cell_arrays()

Get all available cell arrays from the case.

These fields can be used for operations such as selecting
a ColorMap field for rendering.

* **Return List[str]:**
  A list of available cell array names.
* **Return type:**
  [*List*](https://docs.python.org/3/library/typing.html#typing.List)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

#### get_mesh_regions()

Get the currently selected mesh regions in the case.

* **Returns:**
  A list of mesh region names that are currently active.
* **Return type:**
  List[[str](https://docs.python.org/3/library/stdtypes.html#str)]
