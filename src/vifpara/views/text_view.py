import paraview.simple as pv

from ..logging import logger
from ..base import Layout
from . import IViewObject


class TextView(IViewObject):
    def __init__(self, text: str, width: int, height: int, font: str = None, font_size: int = None):
        """
        Initialize a TextView used for rendering text annotations inside a layout cell.

        :param str text: The text content of the annotation.
        :param int width: The width of the text view in pixels.
        :param int height: The height of the text view in pixels.
        :param str font: The font used for the text annotation. Defaults to ``"Arial"``.
            Other options include ``"Courier"`` and ``"Times"``.
        :param int font_size: The font size used for rendering the text. Defaults to 18.
        :return: None
        """
        super().__init__(None, width, height)
        self._text = text

        self._font = 'Arial' if font is None else font
        self._font_size = 18 if font_size is None else font_size

    def _render_inside(self, layout: Layout, row: int=0, col: int=0):
        """
        Renders the text view into a cell in the layout.
        Parameters
        ----------
        layout : Layout
            The layout in which the text view is added.
        row : int
            The row index of the layout, in which the text should be visualized.
        col : int
            The column index of the layout, in which the text should be visualized.
        """
        logger.info(f"Rendering text view to <{row}|{col}>.")

        # add text render view to layout
        layout.add_render_view(row, col, self)

        # Create text object and add to render view
        text = pv.Text(registrationName='description')
        text.Text = self._text
        self._display = pv.Show(text, self._render_view, 'TextSourceRepresentation')

        # vertical_center aligns the text vertically in the center of its view.
        vertical_center: float = 0.5 - (self._font_size / self._height)
        # horizontal_center aligns top text horizontally in the center of its view.
        # 0.618 is the golden ratio, which in most modern fonts is the ratio between width and height
        # (_font_size usually is the height of a character)
        # This is only a heuristic, which works on average but not with edge cases, such as
        # "iiiiiiiii" (smallest possible text) or "OOOOOOOOO" (widest possible text)
        horizontal_center: float = 0.5 - (self._font_size * 0.618 * len(self._text) / self._width)

        # define position of text based on slice matrix index
        if col == 0:
            self._display.SetPropertyWithName('WindowLocation', 'Any Location')
            self._display.Position = [0.05, vertical_center]
        elif row == 0:
            self._display.SetPropertyWithName('WindowLocation', 'Any Location')
            self._display.Position = [horizontal_center, vertical_center]

        # set text parameters
        self._display.FontFamily = self._font
        self._display.FontSize = self._font_size

        self._render_view.ResetCamera(True)
