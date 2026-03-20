import paraview.simple as pv
from typing import List, Optional

from ..base import Layout, Case
from ..logging import logger


class IViewObject:
    def __init__(self, case: Optional[Case], width: int, height: int, show_orientation_axis: bool = False):
        """
        Base class for all objects that contain a ParaView render view.

        This class initializes:
          - A render view
          - Default dimensions
          - A display handle (set after rendering)
          - Optional orientation axis visibility
          - A list of modifier callbacks applied before rendering

        :param Case case: The loaded visualization case of the project.
        :param int width: The width of the view in pixels.
        :param int height: The height of the view in pixels.
        :param bool show_orientation_axis: Whether the ParaView orientation axis
            should be displayed in this view.
        :return: None
        """
        self._case = case
        self._width = width
        self._height = height
        self._render_view = pv.CreateRenderView()
        self._display: pv.Show = None
        self._blocks: Optional[List[str]] = None
        self._modifier_callback_list: list = []
        self._show_orientation_axis: bool = show_orientation_axis

    def delete_view(self):
        """
        Delete the underlying render view.

        This method removes the associated ParaView render view from the
        visualization pipeline and logs that the view should no longer be used.

        :return: None
        """
        logger.info(f"Deleting view {self}. View should not be used anymore.")
        pv.Delete(self._render_view)

    def get_case(self) -> Case:
        """
        Return the loaded case this view is based on.

        :return: The loaded case of the view object.
        :rtype: Case
        """
        return self._case

    def get_width(self) -> int:
        """
        Return the width of the view in pixels.

        If the internally stored width is less than or equal to zero, a warning
        is logged and the width is set to a failsafe value of ``10`` to prevent
        division-by-zero issues during rendering.

        :return: The width of the view in pixels.
        :rtype: int
        """
        if self._width <= 0:
            logger.warning(
                f"View {self} has width of {self._width}. "
                "Will set width to 10px pre rendering."
            )
            self._width = 10  # Failsafe to avoid divisions by 0 in case of empty view
        return self._width

    def get_height(self) -> int:
        """
        Return the height of the view in pixels.

        If the internally stored height is less than or equal to zero, a warning
        is logged and the height is set to a failsafe value of ``10`` to prevent
        division-by-zero issues during rendering.

        :return: The height of the view in pixels.
        :rtype: int
        """
        if self._height <= 0:
            logger.warning(
                f"View {self} has height of {self._height}. "
                "Will set height to 10px pre rendering."
            )
            self._height = 10  # Failsafe to avoid divisions by 0 in case of empty view
        return self._height

    def set_blocks(self, blocks: List[str]):
        """
        Set the list of blocks to be displayed in the view.

        This method assigns the provided list of block identifiers to the internal
        ``_blocks`` attribute, determining which blocks are shown in the rendered
        output.

        :param List[str] blocks: A list of block names or identifiers.
        :return: None
        """
        self._blocks = blocks

    def render(self, layout: Layout, row: int = 0, col: int = 0):
        """
        Render the view into the given layout and apply modifiers.

        This method performs the following steps in order:
        1. Validates that ``layout`` is a ``Layout`` instance.
        2. Renders the view's own content via ``_render_inside`` at the specified grid
        position (``row``, ``col``).
        3. Toggles the orientation axes visibility on the underlying render view,
        if available.
        4. Applies all attached render modifiers via ``_render_modifiers``.
        5. If both a display and block selectors are present, applies the block selection
        to the display.

        :param Layout layout: The layout grid where the view should be placed.
        :param int row: Target row index in the layout grid. Defaults to ``0``.
        :param int col: Target column index in the layout grid. Defaults to ``0``.
        :raises TypeError: If ``layout`` is not an instance of ``Layout``.
        :return: None
        """
        if not isinstance(layout, Layout):
            raise TypeError(
                f"Provided a {type(layout).__name__} instead of a layout to a TextView. "
                "Please provide a Layout object."
            )
        self._render_inside(layout, row, col)
        try:
            self._render_view.OrientationAxesVisibility = 1 if self._show_orientation_axis else 0
        except AttributeError:
            pass
        self._render_modifiers()

        if self._display is not None and self._blocks is not None:
            self._display.BlockSelectors = self._blocks

    def get_render_object(self):
        """
        Return the underlying render object.

        This base implementation does not define a render object and logs an
        error indicating that subclasses should override this method.

        :return: Always returns ``None`` in the base class.
        """
        logger.error(f"Render Object not implemented for {self}.")
        return None


    def get_render_view(self):
        """
        Return the underlying ParaView render view.

        This method provides access to the internal ``_render_view`` attribute,
        which represents the ParaView ``RenderView`` used by the view for
        visualization.

        :return: The associated ParaView render view.
        """
        return self._render_view

    def add_modifier_callback(self, callback):
        """
        Used by view object modifiers to add their render callback to the view object.
        """
        self._modifier_callback_list.append(callback)

    def _render_inside(self, layout: Layout, row: int, col: int):
        """
        Interface method to override. Called by the render() method.
        """
        logger.error(f"Rendering not implemented for {self}.")

    def _render_modifiers(self):
        """
        Iterates over all attached modifiers and renders them one by one.
        """
        for callback in self._modifier_callback_list:
            callback(self, self._display)