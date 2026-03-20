import paraview.simple as pv
from ..logging import logger
from ..views import IViewObject
from . import IViewObjectModifier


class AxesGrid(IViewObjectModifier):
    def __init__(self, x_title: str = 'X Axis', y_title: str = 'Y Axis', z_title: str = 'Z Axis',
                 title_font_size: int = 20, font: str = 'Times', label_font_size: int = 16):
        """
        Initialize an AxesGrid modifier used to visualize a 3‑axis coordinate grid.

        The axes AxesGrid can be used to visualize the axes of a 3d visualization,
        or a slice. It can be attached to a view.

        This modifier configures axis titles, fonts, and label sizes for the ParaView
        axes grid displayed in a render view.

        :param str x_title: The title of the x‑axis.
        :param str y_title: The title of the y‑axis.
        :param str z_title: The title of the z‑axis.
        :param int title_font_size: Font size for the axis titles.
        :param str font: Font family used for axis titles. Options include:
            ``"Arial"``, ``"Courier"``, ``"Times"``.
        :param int label_font_size: Font size for the numeric axis labels.
        :return: None
        """
        super().__init__()
        self._x_title = x_title
        self._y_title = y_title
        self._z_title = z_title
        self._title_font_size = title_font_size
        self._font = font
        self._label_font_size = label_font_size

    def render_callback(self, view_object: IViewObject, display: pv.Show):
        """
        Function used to add the axes grid to a display
        """
        logger.info(f"Attaching axes grid to {view_object}.")
        display.DataAxesGrid.GridAxesVisibility = 1
        display.DataAxesGrid.XTitle = self._x_title
        display.DataAxesGrid.YTitle = self._y_title
        display.DataAxesGrid.ZTitle = self._z_title
        display.DataAxesGrid.XTitleFontSize = self._title_font_size
        display.DataAxesGrid.YTitleFontSize = self._title_font_size
        display.DataAxesGrid.ZTitleFontSize = self._title_font_size
        display.DataAxesGrid.XLabelFontSize = self._label_font_size
        display.DataAxesGrid.YLabelFontSize = self._label_font_size
        display.DataAxesGrid.ZLabelFontSize = self._label_font_size
        display.DataAxesGrid.XTitleFontFamily = self._font
        display.DataAxesGrid.YTitleFontFamily = self._font
        display.DataAxesGrid.ZTitleFontFamily = self._font
        view_object.get_render_view().CameraParallelScale = view_object.get_render_view().CameraParallelScale / 0.5 * 0.8
