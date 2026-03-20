
from ..logging import logger
from ..base import Layout, Case
from . import Slice, TextView, SliceMatrixColorType


class SliceMatrix:
    def __init__(self, slices: list[Slice], texts_top: list[str] = None,
                 texts_left: list[str] = None, color_type: SliceMatrixColorType = SliceMatrixColorType.COLOR_CENTERED,
                 height_slice: int = 520, width_text: int = 300, height_color_bar: int = 150, font: str = None,
                 font_size: int = None, text_view_height: int = 100):
        """
        Initialize a SliceMatrix, a structured arrangement of slices with optional
        text annotations and color bar configurations.

        A SliceMatrix can be used to render multiple slices at once into a layout.
        It can additionally render color bars, and descriptive text.

        A SliceMatrix reserves the entire layout and manages its own internal structure.
        No additional views can be added once the layout is dedicated to a slice matrix.

        :param list[Slice] slices: The list of Slice objects that will be rendered.
        :param list[str] texts_top: Text annotations for the top row (one per column).
        :param list[str] texts_left: Text annotations for the left column (one per row).
        :param SliceMatrixColorType color_type: Defines the color bar strategy for the matrix.
        :param int height_slice: Height in pixels of each slice in the matrix.
        :param int width_text: Width in pixels of the left‑side text views (if any).
        :param int height_color_bar: Height in pixels of the color bars in the matrix.
        :param str font: Font used for text annotations (e.g., ``"Times"``, ``"Courier"``, ``"Arial"``).
        :param int font_size: Font size used for text annotations.
        :param int text_view_height: Height in pixels of the top text views.
        :return: None
        """
        self._slices = slices
        self._texts_top = texts_top
        self._texts_left = texts_left
        self._color_type = color_type
        self._text_views = []
        self._height_slice = height_slice
        self._width_text = width_text
        self._height_color_bar = height_color_bar
        self._font = font
        self._font_size = font_size
        self._text_view_height = text_view_height

    def render(self, layout: Layout):
        """
        Render the slice matrix into the provided layout.

        This method organizes and renders:
        - The slice grid
        - Optional top text row
        - Optional left text column
        - Color bars (depending on the slice matrix color mode)

        The layout is modified by inserting additional rows and/or columns
        to accommodate text annotations and color bars as required by the
        chosen SliceMatrixColorType.

        :param Layout layout: The layout into which the slice matrix should be rendered.
        :return: None
        """
        # compute row and col index offset for slice matrix
        slice_row_idx = 0 if self._texts_top is None else 1
        slice_col_idx = 0 if self._texts_left is None else 1

        # Check if we need to add rows for the color bars
        if self._color_type == SliceMatrixColorType.COLOR_FOR_EACH:
            layout.duplicate_rows()
        elif self._color_type == SliceMatrixColorType.COLOR_CENTERED:
            layout.add_single_full_row(1, to_front=False)
        elif self._color_type == SliceMatrixColorType.COLOR_PER_COLUMN:
            layout.add_single_full_row(to_front=False)

        # Check if we need to add a row or column for the text labels
        if self._texts_top is not None:
            layout.add_single_full_row(to_front=True)
        if self._texts_left is not None:
            layout.add_single_full_column()

        # We need a dummy element for the corner when top and left text is enabled
        if self._texts_left is not None and self._texts_top is not None:
            self._texts_top.insert(0, "")

        # render slice based on row and col starting index
        if self._color_type == SliceMatrixColorType.COLOR_FOR_EACH:
            self._render_slices_for_each(layout, slice_row_idx, slice_col_idx)
        else:
            self._render_slices(layout, slice_row_idx, slice_col_idx)

        # check color map render config
        if self._color_type is not SliceMatrixColorType.COLOR_NONE:
            if self._color_type == SliceMatrixColorType.COLOR_CENTERED:
                # render one centered color bar
                self._render_centered_color_map(layout, slice_col_idx)
            elif self._color_type == SliceMatrixColorType.COLOR_PER_COLUMN:
                # render color map for each column
                self._render_column_color_map(layout, slice_col_idx)
            elif self._color_type == SliceMatrixColorType.COLOR_FOR_EACH:
                pass
            else:
                logger.error("Unknown slice matrix color type.")

        # render first row of texts
        if self._texts_top is not None:
            self._render_texts_top(layout, slice_col_idx)

    # private function to render the slices
    def _render_slices(self, layout, slice_row_idx: int, slice_col_idx: int):
        slice_idx = 0

        col_text_id: int = 0
        # Iterate through all slice rows in layout
        for i in range(slice_row_idx, len(layout.get_cell_array())):

            if slice_col_idx != 0:
                # Add text in first column
                self._add_col_text_to_matrix(layout, i, 0, col_text_id)
                col_text_id += 1

            # Add slices in remaining columns of row
            for j in range(slice_col_idx, layout.get_cell_array()[i]):
                # Render slice at given layout cell index.
                if slice_idx >= len(self._slices):
                    continue
                self._slices[slice_idx].render(layout=layout, row=i, col=j)
                slice_idx = slice_idx + 1

    # private function for adding the slices and color bars for each slice
    def _render_slices_for_each(self, layout, slice_row_idx, slice_col_idx):
        slice_idx = 0

        col_text_id: int = 0
        # Iterate through all slice rows in layout
        for i in range(slice_row_idx, len(layout.get_cell_array()), 2):
            if slice_col_idx != 0:
                # Add text in first column
                self._add_col_text_to_matrix(layout, i, 0, col_text_id)
                self._add_empty_text(layout, i + 1, 0)
                col_text_id += 1

            # Add slices in remaining columns of row
            for j in range(slice_col_idx, layout.get_cell_array()[i]):
                # Render slice at given layout cell index.
                self._slices[slice_idx].render(layout=layout, row=i, col=j)
                self._slices[slice_idx].set_color_bar_size(height=self._height_color_bar,
                                                         width=self._slices[slice_idx].get_width())
                self._slices[slice_idx].render_color_bar(layout=layout, row=i + 1, col=j)
                slice_idx = slice_idx + 1

    # private function for adding the text annotations on the left to the matrix
    def _add_col_text_to_matrix(self, layout, row_idx, col_idx, col_text_id: int):
        if col_text_id >= len(self._texts_left):
            self._add_empty_text(layout, row_idx, col_idx)
            return
        text_view_obj = TextView(text=self._texts_left[col_text_id], width=self._width_text,
                                 height=self._height_slice, font=self._font,
                                 font_size=self._font_size)
        text_view_obj.render(layout=layout, row=row_idx, col=col_idx)
        self._text_views.append(text_view_obj)

    # private function for adding the text annotations in the first row
    def _render_texts_top(self, layout, slice_col_idx):
        # Add first row of text
        if slice_col_idx != 0:
            text_view_obj = TextView(text=self._texts_top[0], width=self._width_text,
                                     height=self._text_view_height, font=self._font,
                                     font_size=self._font_size)
            text_view_obj.render(layout=layout, row=0, col=0)
            self._text_views.append(text_view_obj)

        # Iterate over first row
        for i in range(slice_col_idx, layout.get_cell_array()[0]):
            text_view_obj = TextView(text=self._texts_top[i],
                                     width=self._slices[i - slice_col_idx].get_width(),
                                     height=self._text_view_height, font=self._font,
                                     font_size=self._font_size)
            text_view_obj.render(layout=layout, row=0, col=i)
            self._text_views.append(text_view_obj)

    # private function for adding an empty text in the last row
    def _add_empty_text(self, layout, row_idx, col_idx):
        text_view_obj = TextView(text="", width=self._width_text,
                                 height=self._height_color_bar)
        text_view_obj.render(layout=layout, row=row_idx, col=col_idx)
        self._text_views.append(text_view_obj)

    # private function for rendering a centered color bar
    def _render_centered_color_map(self, layout, col_idx):
        # compute sum of slice x resolutions
        width = sum([self._slices[i].get_width() for i in range(layout.get_cell_array()[0] - col_idx)])
        # Render color bar centered in last row
        self._slices[0].set_color_bar_size(width=width, height=self._height_color_bar)
        self._slices[0].render_color_bar(layout=layout, row=len(layout.get_cell_array()) - 1, col=col_idx)

    # private function for adding a color bar per column
    def _render_column_color_map(self, layout, col_idx):
        for i in range(layout.get_cell_array()[0] - col_idx):
            self._slices[i].set_color_bar_size(width=self._slices[i].get_width(), height=self._height_color_bar)
            self._slices[i].render_color_bar(layout=layout, row=len(layout.get_cell_array()) - 1, col=col_idx + i)
