import paraview.simple as pv

from ..logging import logger

from . import IViewObject, ColorMap
from ..base import Layout


class ColorBarView(IViewObject):
    def __init__(self, width: int, height: int, slice_obj: pv.Slice,
                 color_map=None, slice_type='Plane'):
        """
        Initialize a ColorBarView instance.

        This class is used internally by the ``Slice`` class to render a
        corresponding color bar. It should not be instantiated directly by users.

        :param int width: The width of the color bar view in pixels.
        :param int height: The height of the color bar view in pixels.
        :param pv.Slice slice_obj: The ParaView slice object from which scalar
            values and their color range are obtained.
        :param ColorMap color_map: The color map applied to the color bar.
        :param str slice_type: The type of slice used by the parent slice object.
        :return: None
        """
        super().__init__(None, width, height)
        self._color_map = color_map
        self._slice_type = slice_type
        self._slice_obj = slice_obj
        self._origin = None
        self._normal = None

    def set_size(self, width: int, height: int):
        """
        Set the size of the color bar view.

        :param int width: The new width in pixels.
        :param int height: The new height in pixels.
        :return: None
        """
        self._width = width
        self._height = height

    def set_coordinates(self, origin, normal):
        """
        Set the origin and normal vector for the slice that the color bar corresponds to.

        :param origin: The origin of the slice (typically a 3‑element list or Vector3).
        :param normal: The normal vector of the slice.
        :return: None
        """
        self._origin = origin
        self._normal = normal

    def _render_inside(self, layout: Layout, row: int, col: int):
        logger.info("Rendering slice color bar.")
        # add color bar render view to layout
        layout.add_render_view(row, col, self)

        # create slice based on origin, normal and type
        pv.SetActiveView(None)
        pv.SetActiveView(self._render_view)

        # configure slice
        self._slice_obj.SliceType = self._slice_type
        self._slice_obj.SliceType.Origin = self._origin.to_list()
        self._slice_obj.SliceType.Normal = self._normal.to_list()

        # assign slice to render-view
        slice_display = pv.Show(self._slice_obj, self._render_view)

        # hide slice object in color bar view
        pv.Hide(self._slice_obj, self._render_view)

        # add color legend
        if self._color_map is not None:
            self._color_map.apply_to_render_view(slice_display, self._render_view, True)

        return slice_display