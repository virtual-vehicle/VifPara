import paraview.simple as pv
import vtk
from typing import List, Tuple, Optional, Union
from ..logging import logger
from . import CaseType, Config


class Case:
    def __init__(self, *, config: Config, loader: str = "openfoam", case_type: CaseType = CaseType.RECONSTRUCTED):
        """
        Initialize a new case and load it using the specified ParaView reader.

        The case is the central object everything revolves around. Create it by passing
        a config instance with the correct case path. Then you can set the loader to load OpenFoam or MeshFree cases.

        :param Config config: The preloaded configuration object providing the case path.
        :param LoaderType loader: The reader type to use. Can be "openfoam", "ensight", or "file". Capitalization does
               not matter. The "file" specifier allows to read arbitrary file types, such as stl, vtu, pvd
        :param CaseType case_type: The type of case to load (e.g., reconstructed).
        :return: None
        :raises TypeError: If the loader is incompatible with the case type.
        """
        logger.info("Creating new case.")

        self.loader: str = loader.lower()
        self.case_type: CaseType = case_type
        self._case = None

        # For backwards compatibility, openfoam is still a valid parameter, even though it falls into the "file"
        # classification.
        if self.loader == "openfoam":
            self._case = pv.OpenFOAMReader(FileName=config.get_case_path(), CaseType=int(case_type))
        elif self.loader == "ensight":
            self._case = pv.EnSightReader(CaseFileName=config.get_case_path())
        elif self.loader == "file":
            self._case = pv.OpenDataFile(filename=config.get_case_path())
        else:
            raise TypeError("Invalid loader type provided to Case constructor.")

        if self._case is None:
            raise TypeError(f"Wrong loader type provided. You used {self.loader} for {config.get_case_path()}.")

        self._case.UpdatePipelineInformation()
        self._time_step_count: int = len(self._case.TimestepValues)
        self._updated: bool = False
        self._case_view = pv.CreateRenderView()
        self._case_display: pv.Show = pv.Show(self._case, self._case_view)

        #logger.debug(self._case_display.BlockSelectors)
        #logger.debug(self._case.GetDataInformation().DataInformation.GetBlockName(1).decode("utf-8", errors="ignore").split(" ")[0])

        logger.info(f"Case contains {self._time_step_count} time steps.")

    def get_blocknames(self):
        """
        Get all multiblock names from the case.
        :return List[str]: A list containing the hierarchical names of all blocks in the dataset's VTK data assembly.
        """
        assembly: vtk.vtkDataAssembly = self._case.GetDataInformation().GetHierarchy()
        if assembly is None:
            return None
        blocknames: List[str] = []
        max_iterations: int = 10_000
        for i in range(max_iterations):
            new_name: str = assembly.GetNodePath(i)
            if new_name == "":
                break

            blocknames.append(new_name)
        return blocknames

    def log_blocknames(self):
        """
        Log all multiblock names available in the case.

        This prints a formatted list of all block names to the application logger.

        :return: None
        """
        blocknames: List[str] = self.get_blocknames()
        if blocknames is None:
            blocknames_string = "No blocknames in loaded case."
        else:
            blocknames_string = "\n".join(
                f"    {blockname}"
                for blockname in blocknames
            )

        blocknames_string = "----- Available blocknames -----\n" + blocknames_string
        logger.info(blocknames_string)

    def get_case(self):
        """
        Get the underlying ParaView case object.

        :return: The internal ParaView data source representing the loaded case.
        """
        return self._case

    def set_mesh_regions(self, mesh_regions: List[str]):
        """
        Set the mesh regions that determine which parts of the case are rendered.

        :param List[str] mesh_regions: A list of region names to be rendered.Common default is ``["internalMesh"]``.
        :return: None
        """
        try:
            self._case.MeshRegions = mesh_regions
            self._case.UpdatePipeline()
        except AttributeError as e:
            logger.error(f"One of the following mesh regions do not exist in the loaded case: {mesh_regions}.")


    def get_range(self, field_name: str, force_update: bool = False) -> Optional[Tuple[float, float]]:
        """
        Get the minimum and maximum values of a scalar field in the loaded case.

        This method searches first in point data and then in cell data.  
        If the field does not exist, ``None`` is returned.  
        On the first call, or when ``force_update`` is ``True``, the pipeline is updated
        which may take additional time.

        :param str field_name: The name of the scalar field whose value range should be extracted.
        :param bool force_update: If ``True``, forces a pipeline update before reading the field range.
        :return Optional[Tuple[float, float]]: A ``(min, max)`` tuple representing the field range, or ``None`` if the field is not found.
        """
        logger.info(f"Fetching range from {field_name}.")
        if not self._updated or force_update:
            self._case.UpdatePipeline()
            self._updated = True
        info = self._case.GetDataInformation()

        # ParaView tracks point and cell data separately
        pd_info = info.GetPointDataInformation()
        cd_info = info.GetCellDataInformation()

        # Try point data first, then cell data
        for dset in (pd_info, cd_info):
            for i in range(dset.GetNumberOfArrays()):
                arr_info = dset.GetArrayInformation(i)
                if arr_info.GetName() == field_name:
                    return arr_info.GetComponentRange(-1)  # (-1) → magnitude range or scalar range

        logger.error(f"Field '{field_name}' not found in point or cell data. Returning None.")
        return None

    def set_point_arrays(self, point_arrays: List[str]):
        """
        Set the active point arrays for the case.

        :param List[str] point_arrays: A list of point array names to enable on the data source.
        :return: None
        """
        self._case.PointArrays = point_arrays

    def set_cell_arrays(self, cell_arrays: List[str]):
        """
        Set the active cell arrays for the case.

        :param List[str] cell_arrays: A list of cell array names to enable on the data source.
        :return: None
        """
        self._case.CellArrays = cell_arrays

    def get_time_step_count(self) -> int:
        """
        Get the number of available time steps in the loaded case.

        :return int: The total number of time steps.
        """
        return self._time_step_count

    def log_patch_array_info(self):
        """
        Log all available mesh regions and their current selection status.

        The output lists each mesh region along with its activation flag
        and is written to the application logger.

        :return: None
        """
        patch_array_info: List[dict] = self.get_patch_array_info()
        if patch_array_info is None:
            patch_array_string = "No mesh regions in loaded case."
        else:
            patch_array_string = "\n".join(
                f"    {patch['name']}: {patch['status']}"
                for patch in patch_array_info
            )

        patch_array_string = "----- Available mesh regions -----\n" + patch_array_string
        logger.info(patch_array_string)

    def log_cell_arrays(self):
        """
        Log all available cell arrays.

        This prints a formatted list of cell array names to the application logger,
        allowing the user to inspect which fields are available for cell‑based operations.

        :return: None
        """
        cell_arrays: List[str] = self.get_cell_arrays()
        if cell_arrays is None:
            cells_string = "No cell array in loaded case."
        else:
            cells_string = "\n".join(
                f"    {single_cell}"
                for single_cell in cell_arrays
            )

        cells_string = "----- Available cell arrays -----\n" + cells_string
        logger.info(cells_string)

    def log_point_arrays(self):
        """
        Log all available point arrays.

        This prints a formatted list of point array names to the application logger,
        allowing inspection of which point-based fields are available.

        :return: None
        """
        point_arrays: List[str] = self.get_point_arrays()
        if point_arrays is None:
            points_string = "No point arrays in loaded case."
        else:
            points_string = "\n".join(
                f"    {single_cell}"
                for single_cell in point_arrays
            )

        points_string = "----- Available point arrays -----\n" + points_string
        logger.info(points_string)

    def get_point_arrays(self) -> List[str]:
        """
        Get the list of available point arrays from the case.

        :return List[str]: A list of point array names provided by the data source.
        """
        return self._case.GetProperty("PointArrays")

    def get_patch_array_info(self) -> List[dict]:
        """
        Get all available mesh regions and their activation status.

        Each entry contains:
        - ``name`` (str): The mesh region name.
        - ``status`` (int): ``1`` if selected, ``0`` if not selected.

        :return List[dict]: A structured list containing information about all mesh regions and whether each region is currently active.
        """
        array_info: List[str] = self._case.GetProperty("PatchArrayInfo")
        if array_info is None:
            return []
        structured_array_info: List[dict] = []
        for idx, val in enumerate(array_info):
            if idx % 2 != 0:
                continue
            name: str = array_info[idx]
            status: int = int(array_info[idx + 1])
            structured_array_info.append({"name": name, "status": status})
        return structured_array_info

    def get_cell_arrays(self) -> List[str]:
        """
        Get all available cell arrays from the case.

        These fields can be used for operations such as selecting
        a ColorMap field for rendering.

        :return List[str]: A list of available cell array names.
        """
        return self._case.GetProperty("CellArrays")

    def get_mesh_regions(self):
        """
        Get the currently selected mesh regions in the case.

        :return: A list of mesh region names that are currently active.
        :rtype: List[str]
        """
        return self._case.MeshRegions

