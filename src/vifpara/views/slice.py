import paraview.simple as pv
import numpy as np
from typing import List

from ..logging import logger
from ..other import Vector3
from ..other.utils import intersect_vector_bounding_box
from ..base import Case, Layout
from . import IViewObject, ColorBarView, ColorMap


class Slice(IViewObject):
    def __init__(self, *, case: Case,
                 origin: Vector3 = Vector3(0.0, 0.0, 1.0),
                 normal: Vector3 = Vector3(1.0, 0.0, 0.0),
                 camera_up: Vector3 = Vector3(0.0, 0.0, 1.0),
                 slice_type='Plane', height=135, color_map=None,
                 margin_x: int = 0, margin_y: int = 0, offset_x: int = 0,
                 offset_y: int = 0, zoom=1.0, show_orientation_axis: bool = False,
                 representation_type: str = "Surface", representation_point_size: float = 1.0):
        """
        Initialize a Slice object used to extract and visualize a planar slice
        from a loaded dataset.

        The Slice represents a 2 dimensional rendered plane through a case.
        It can be used to see "inside" a case. It can be zoomed, offset, etc.

        :param Case case: The loaded VifPara case.
        :param Vector3 origin: The origin point of the slice plane.
        :param Vector3 normal: The normal vector defining the slice plane direction.
        :param Vector3 camera_up: The camera's up-vector inside the slice view.
        :param str slice_type: The type of slice (e.g., ``"Plane"``).
        :param int height: The height of the screenshot in pixels.
        :param ColorMap color_map: The color mapping configuration. If ``None``,
            the slice is displayed with a default gray color.
        :param int margin_x: Optional horizontal margin (positive = wider image,
            negative = tighter crop).
        :param int margin_y: Optional vertical margin (positive = taller image,
            negative = tighter crop).
        :param int offset_x: Horizontal camera shift. Positive moves the camera right,
            negative left.
        :param int offset_y: Vertical camera shift. Positive moves the camera down,
            negative up.
        :param float zoom: Zoom factor for the 3D visualization (2.0 = 2× larger,
            0.5 = half size).
        :param bool show_orientation_axis: Whether to show the orientation axis widget.
        :param str representation_type: The data representation type (``"Surface"`` or ``"Points"``).
        :param float representation_point_size: Point size when using point-based representations.
        :return: None
        """
        super().__init__(case, 263, height, show_orientation_axis)
        self._case = case
        self._origin: Vector3 = origin
        self._normal: Vector3 = normal
        self._camera_up: Vector3 = camera_up
        self._type: str = slice_type
        self._representation_type = representation_type
        self._representation_point_size = representation_point_size
        self._color_map: ColorMap = color_map
        self._slice_obj: pv.Slice = pv.Slice(Input=self._case.get_case())
        self._color_bar: ColorBarView = ColorBarView(100, 100, self._slice_obj, color_map, slice_type)
        self._camera_scale: float = 1.0 / zoom
        self._margin_x: int = int(margin_x)
        self._margin_y: int = int(margin_y)
        self._offset_x: int = int(offset_x)
        self._offset_y: int = int(offset_y)

        self._prepare_dimensions()
    
    @staticmethod
    def generate_slice_array(case: Case, generator_direction: Vector3, num_slices: int, **kwargs) -> List["Slice"]:
        """
        Generate an array of Slice objects placed along a direction vector.

        This static method automatically computes a sequence of slice origins along the
        bounding box of the given case. It is useful for exploring datasets by quickly
        generating multiple evenly spaced slices through the domain.

        Any keyword arguments valid for the Slice constructor may be passed, except
        ``origin`` which is ignored because origins are auto‑generated.  
        If ``normal`` is not provided, the ``generator_direction`` is used as the slice normal.

        :param Case case: The case in which slices will be generated.
        :param Vector3 generator_direction: The direction along which the slices are placed.  
            If no ``normal`` is provided via kwargs, this vector will be used.
        :param int num_slices: The number of slices to generate. Higher values lead to
            finer spacing along the generator direction.
        :param kwargs: Additional keyword arguments forwarded to the Slice constructor
            (e.g., ``color_map=cmap``, ``camera_up=Vector3.forward()``).  
            The keyword ``origin`` is not allowed and will be ignored.
        :return List[Slice]: A list containing all generated Slice instances.
        """
        logger.info(f"Generating slice array in {generator_direction} direction.")

        case.get_case().UpdatePipeline()
        norm_direction = generator_direction.normalized()
        (x_min, x_max, y_min, y_max, z_min, z_max) = case.get_case().GetDataInformation().GetBounds()

        case_center: Vector3 = Vector3(
            (x_max + x_min) / 2,
            (y_max + y_min) / 2,
            (z_max + z_min) / 2
        )

        start_origin, end_origin = intersect_vector_bounding_box(
            case_center, generator_direction,
            (x_min, x_max, y_min, y_max, z_min, z_max)
        )

        # Compute vector representing step for each slice
        distance: float = (end_origin - start_origin).magnitude()
        delta_magnitude: float = distance / num_slices
        delta_vector: Vector3 = norm_direction * delta_magnitude

        slice_array: List["Slice"] = []

        # If a normal is provided, use it; otherwise use generator_direction
        if "normal" in kwargs:
            normal = kwargs["normal"]
            del kwargs["normal"]
        else:
            logger.info("No normal argument provided to generate_slice_array(). "
                        "Will use generator_direction instead.")
            normal = generator_direction

        # Ignore a provided origin, because this method computes origins automatically
        if "origin" in kwargs:
            logger.warning("origin argument in generate_slice_array() is ignored. "
                        "Slices will be generated based on the case center.")
            del kwargs["origin"]

        for i in range(num_slices):
            curr_origin: Vector3 = start_origin + (delta_vector * i)
            logger.info(f"    {i}. Generating slice on {curr_origin}")
            new_slice: "Slice" = Slice(case=case, origin=curr_origin, normal=normal, **kwargs)
            slice_array.append(new_slice)

        return slice_array

    def _render_inside(self, layout: Layout, row: int=0, col: int=0):
        """
        Renders the slice into a cell in the layout.

        Parameters:
        ----------
        layout: Layout
            The layout to render the slice in.
        row: int
            The row to render the slice in.
        col: int
            The col in the given row to render the slice in.
        """
        logger.info(f"Rendering slice to <{row}|{col}>.")

        layout.add_render_view(row, col, self)

        # create slice based on origin, normal and type
        pv.SetActiveView(None)
        pv.SetActiveView(self._render_view)

        # add color legend
        if self._color_map is not None:
            self._color_map.apply_to_render_view(self._display, self._render_view, False)
        else:
            pv.ColorBy(self._display, None)

    def set_color_bar_size(self, height: int = None, width: int = None):
        """
        Set the size of the color bar view for the slice.

        If no value is provided:
        - ``height`` defaults to ``80`` pixels.
        - ``width`` defaults to the width of the slice view.

        :param int height: The height of the color bar in pixels. If ``None``, the default
            height of ``80`` px is used.
        :param int width: The width of the color bar in pixels. If ``None``, the width of
            the slice view is used.
        :return: None
        """
        # Default value of height and width is None due to unification reasons of the signature.
        # We could set height = 80 as default, but width needs to be None to set it to the width of the slice.
        if height is None:
            height = 80  # Default number for default height (in px) of color bar
        if width is None:
            width = self._width
        self._color_bar.set_size(width, height)

    def render_color_bar(self, layout: Layout, row: int = 0, col: int = 0):
        """
        Render the slice's color bar into a specific cell of the layout.

        :param Layout layout: The layout into which the color bar should be rendered.
        :param int row: The target row index in the layout.
        :param int col: The target column index within the selected row.
        :return: None
        """
        self._color_bar.set_coordinates(self._origin, self._normal)
        self._color_bar.render(layout, row, col)

    def get_color_map(self):
        return self._color_map

    def get_color_bar(self):
        return self._color_bar

    def get_origin(self):
        return self._origin

    def get_camera_up(self):
        return self._camera_up

    def get_normal(self):
        return self._normal

    def get_render_color_view(self):
        return self._color_bar.get_render_view()

    def get_render_object(self):
        return self._slice_obj

    def _prepare_dimensions(self):
        # create slice based on origin, normal and type
        pv.SetActiveView(None)
        pv.SetActiveView(self._render_view)

        self._slice_obj.SliceType = self._type
        self._slice_obj.SliceType.Origin = self._origin.to_list()
        self._slice_obj.SliceType.Normal = self._normal.to_list()

        # assign slice to render-view
        self._display = pv.Show(self._slice_obj, self._render_view)
        self._display.SetRepresentationType(self._representation_type)
        self._display.PointSize = self._representation_point_size

        # compute bounds and extents
        (x_min, x_max, y_min, y_max, z_min, z_max) = self._slice_obj.GetDataInformation().GetBounds()
        slice_extends = Vector3(x_max - x_min, y_max - y_min, z_max - z_min)

        # base focal point (center of slice)
        base_focal_point = slice_extends / 2.0 + Vector3(x_min, y_min, z_min)

        # calculate camera coordinate system
        y_size = abs(self._camera_up.dot(slice_extends))
        if y_size == 0:
            y_size = 10
        y_dir = self._camera_up.normalized()
        x_dir = self._camera_up.cross(self._normal).normalized()
        x_size = abs(x_dir.dot(slice_extends))
        if x_size == 0:
            x_size = 10
        x_res = round(x_size * self._height / y_size)

        # apply offset in camera space
        offset_vector = x_dir * self._offset_x + y_dir * self._offset_y

        self._render_view.CameraFocalPoint = (base_focal_point + offset_vector).to_list()
        self._render_view.CameraPosition = (np.array(self._render_view.CameraFocalPoint) -
                                            np.array(self._normal.to_list())).tolist()
        self._render_view.CameraViewUp = self._camera_up.to_list()
        self._render_view.CameraParallelProjection = 1

        # store original dimensions
        original_height = self._height

        # update with margins
        self._width = x_res + self._margin_x
        self._height += self._margin_y

        # scale factor to compensate for margins
        height_scale_factor = self._height / original_height

        # base camera scale
        base_camera_scale = y_size * 0.5

        base_camera_scale *= self._camera_scale

        # apply compensated camera scale
        self._render_view.CameraParallelScale = base_camera_scale * height_scale_factor