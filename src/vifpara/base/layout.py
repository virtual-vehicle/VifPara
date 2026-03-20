import sys
from dataclasses import dataclass
import paraview.simple as pv

from ..logging import logger


@dataclass
class ScaleIdEntry:
    scale_id: int = -1
    inv_fraction: bool = False

    def __init__(self, scale_id: int, inv_fraction: bool):
        self.scale_id = scale_id
        self.inv_fraction = inv_fraction

    def get_fraction(self, fraction: float) -> float:
        if self.inv_fraction:
            return 1.0 - fraction
        else:
            return fraction



class Layout:
    def __init__(self, cell_array: list):
        """
        Initialize a layout used as the basis for image and animation exports.

        The layout is the basic building block for visualization.
        Use it to render one or multiple views or a slice matrix.
        Then you can pass the layout to an exporter to export it as images or animations.

        A layout consists of rows and columns of view cells. Each cell will contain
        one rendered view. All cells must be assigned a view before exporting,
        otherwise the export will fail.

        Example:
            A ``cell_array`` like ``[3, 2, 4]`` creates a layout with three rows:
            - Row 1 contains 3 cells
            - Row 2 contains 2 cells
            - Row 3 contains 4 cells

        :param list cell_array: A descriptor defining the number of columns (cells)
            in each row of the layout.
        :return: None
        """
        self._layout = None

        self._y_resolution = None

        self._cell_array = [1]

        # create rows array
        self._rows = [[0]]

        # We need those to track which ids we need to adapt the width and height of each cell.
        # The layout is stored as an SB tree, where each view is a leaf. Each split-edge is an intermediate
        # node.
        self._height_ids: dict = {}
        self._width_ids: dict = {}
        self._views: dict = {}
        self._export_prepared = False

        self.update_layout(cell_array)

        logger.info(f"Prepared layout with dimensions: {cell_array}.")

    def delete_layout(self):
        """
        Delete the current layout from ParaView.

        This removes the internal ParaView layout object and marks it as unusable.
        After this call, the layout should no longer be used.

        :return: None
        """
        logger.info(f"Deleting layout {self}. Layout should not be used anymore.")
        pv.Delete(self._layout)

    def set_height(self, height: int):
        """
        Set the height of the layout, which determines the resolution of exported images or animations.

        The width is automatically computed based on this height.  
        This is required because ParaView can break the layout configuration when exporting images
        larger than the physical screen size, so controlling the resolution avoids this issue.

        :param int height: The height of the exported image in pixels.
        :return: None
        """
        self._y_resolution = height

    def update_layout(self, cell_array):
        self._reset_layout()

        self._cell_array = cell_array

        # create rows array
        self._rows = [[0]]

        self._height_ids: dict = {}
        self._width_ids: dict = {}
        self._views: dict = {}
        self._export_prepared = False

        # clamp rows and cols parameters
        num_rows = max(0, len(cell_array) - 1)

        # create rows
        for i in range(0, num_rows):
            self._add_row()

        # create cols
        for i in range(0, len(self._rows)):
            for j in range(0, cell_array[i] - 1):
                self._add_column(i)

    def set_view_width(self, view, fraction: float):
        self._set_cell_width_by_id(self.get_view_id(view), fraction)

    def set_view_height(self, view, fraction: float):
        self._set_cell_height_by_id(self.get_view_id(view), fraction)

    def set_cell_width(self, row_index: int, column_index: int, fraction: float):
        self._set_cell_width_by_id(self.get_cell_index_row_column(row_index, column_index), fraction)

    def set_cell_height(self, row_index: int, column_index: int, fraction: float):
        self._set_cell_height_by_id(self.get_cell_index_row_column(row_index, column_index), fraction)

    def get_view_id(self, view) -> int:
        return self._layout.GetViewLocation(view)

    def get_view(self, row: int, column: int):
        view_id: int = self.get_cell_index_row_column(row, column)
        return self._views[view_id]

    def prepare_export(self):
        if self._export_prepared:
            return # For safety measures, let's not prepare the same layout multiple times.
        if len(self._views) == 0:
            logger.error("No views rendered inside the layout. Cannot prepare for export. Did you forget to call render() for each view object?")
            return

        if not self._all_cells_filled():
            logger.error("Not all layout cells are filled with view objects."
                         "Please either add more views, or remove cells from the layout.")
            return

        self._export_prepared = True
        image_height: int = self._y_resolution
        if image_height is None:
            self.set_height(800) # Default value 800 px on the y axis of the image.
            image_height: int = self._y_resolution

        computed_width: int = self._get_layout_width()
        computed_height: int = self._get_layout_height()
        image_width = int(float(image_height) * float((float(computed_width) / float(computed_height))))

        logger.info(f"Exported layout image has width {image_width}px and height {image_height}px.")

        self._set_cell_height_fractions(image_height, computed_height)
        self._set_cell_width_fractions(image_width, computed_width)
        self._layout.SetSize(image_width, image_height)

    def get_layout(self):
        return self._layout

    def get_cell_index_row_column(self, row_index: int, column_index: int):
        try:
            return self._rows[row_index][column_index]
        except IndexError:
            logger.error("Layout has no cell with indices (" + str(row_index) + ", " + str(column_index) + ")")
            sys.exit(0)

    def get_cell_index(self, index):
        try:
            row_index = int(index / len(self._rows[0]))
            col_index = index % len(self._rows[0])
            return self._rows[row_index][col_index]
        except IndexError:
            logger.error("Layout has no cell with index " + str(index))
            sys.exit(0)

    def get_cell_array(self):
        return self._cell_array

    def add_render_view(self, row: int, col: int, view_object: "IViewObject"):
        self._views[self.get_cell_index_row_column(row_index=row, column_index=col)] = view_object
        self._layout.AssignView(self.get_cell_index_row_column(row_index=row, column_index=col), view_object.get_render_view())

    def add_single_full_row(self, col_number: int = 0, to_front: bool = False):
        new_cell_array: list = self._cell_array

        new_value: int = col_number
        if col_number == 0:
            new_value = self._cell_array[0]

        if to_front:
            new_cell_array.insert(0, new_value)
        else:
            new_cell_array.append(new_value)
        self.update_layout(new_cell_array)

    def add_single_full_column(self):
        new_cell_array: list = self._cell_array

        for i in range(len(new_cell_array)):
            new_cell_array[i] += 1
        self.update_layout(new_cell_array)

    def duplicate_rows(self):
        new_cell_array: list = []
        for row in self._cell_array:
            new_cell_array.append(row)
            new_cell_array.append(row)
        self.update_layout(new_cell_array)

    def _set_cell_width_by_id(self, cell_id, fraction: float):
        if cell_id not in self._width_ids:
            # If no cell_id was found, the row was never split. That is ok, just leave it with 100% size.
            return
        width_id: ScaleIdEntry = self._width_ids[cell_id]
        self._layout.SetSplitFraction(width_id.scale_id, width_id.get_fraction(fraction))

    def _set_cell_height_by_id(self, cell_id, fraction: float):
        if cell_id not in self._height_ids:
            # If no cell_id was found, the image was never split in multiple rows. This indicates a single image and is ok.
            return
        height_id: ScaleIdEntry = self._height_ids[cell_id]
        self._layout.SetSplitFraction(height_id.scale_id, height_id.get_fraction(fraction))

    def _all_cells_filled(self) -> list:
        num_cells: int = 0
        for row in self._rows:
            num_cells += len(row)
        return len(self._views) == num_cells

    def _reset_layout(self):
        self._layout = None
        self._layout = pv.CreateLayout(name='Layout Slice Matrix')

    # private function for adding a row to the layout
    def _add_row(self):
        last_row = self._rows[-1]
        new_index = self._layout.SplitVertical(last_row[0], 0.5)
        self._rows = [x for x in self._rows[:-1]] + [[new_index], [new_index + 1]]

        # For each child in the SB tree we check the parent. This parent is the id we need to edit the height of the cells.
        self._height_ids[new_index] = ScaleIdEntry(last_row[0], False)
        self._height_ids[new_index + 1] = ScaleIdEntry(last_row[0], False)

    # private function for adding a column to the layout
    def _add_column(self, row_index):
        row = self._rows[row_index]
        new_index = self._layout.SplitHorizontal(row[-1], 0.5)
        self._rows[row_index] = [x for x in row[:-1]] + [new_index, new_index + 1]

        # For each child in the SB tree we check the parent. This parent is the id we need to edit the width of the cells.
        self._width_ids[new_index] = ScaleIdEntry(row[-1], False)
        self._width_ids[new_index + 1] = ScaleIdEntry(row[-1], False)
        # Now we also get the height ids for each new cell from the height id of the parent.
        # This ONLY works because we first split the rows of the layout, and AFTERWARDS the columns.
        if len(self._height_ids) > 0:
            self._height_ids[new_index] = ScaleIdEntry(self._height_ids[row[-1]].scale_id, False)
            self._height_ids[new_index + 1] = ScaleIdEntry(self._height_ids[row[-1]].scale_id, False)
            # Prune old leaves out of the height ids dictionary, since we do not want to edit those edges.
            self._height_ids.pop(row[-1])

    def _get_layout_width(self) -> int:
        max_width: int = 0
        for row in self._rows:
            curr_width: int = 0
            for cell_id in row:
                cell_width: int = self._views[cell_id].get_width()
                curr_width += cell_width
            if curr_width > max_width:
                max_width = curr_width
        return max_width

    def _get_layout_height(self) -> int:
        curr_height: int = 0
        for row in self._rows:
            row_height: int = self._views[row[0]].get_height()
            curr_height += row_height
        return curr_height

    def _get_cumulative_height(self, start_row_idx: int, end_row_idx: int) -> int:
        cumulative_height: int = 0
        if start_row_idx < 0:
            start_row_idx = 0
        for i in range(start_row_idx, end_row_idx+1):
            row = self._rows[i]
            cell_id = row[0]
            cell_view = self._views[cell_id]
            cumulative_height += cell_view.get_height()
        return cumulative_height

    def _set_cell_height_fractions(self, image_height: int, max_height: int):
        """
        Computes the relative fraction for each row based on the total fraction of the next rows.
        This is required because of the tree structure of the layout.
        It first computes the absolute fraction of each row height based on the total window height.
        Next, it computes the relative fractions of each row by dividing its own absolute fraction by the
        cumulative absolute fraction of all next rows. This allows for a one pass fraction assignment to all
        rows.
        """
        # Height fetching
        height_list: list = []
        for i, row in enumerate(self._rows):
            cell_id = row[0]
            cell_view = self._views[cell_id]
            height: int = cell_view.get_height()
            height_list.append(height)

        # Absolute fraction computation
        abs_height_fraction_list: list = []
        for height_idx, curr_height in enumerate(height_list):
            abs_height_fraction = curr_height / image_height * (image_height / max_height)
            abs_height_fraction_list.append(abs_height_fraction)

        # Relative fraction computation
        rel_height_fraction_list: list = []
        for height_idx, curr_height in enumerate(abs_height_fraction_list):
            rel_height_fraction = curr_height / sum(abs_height_fraction_list[height_idx:])
            rel_height_fraction_list.append(rel_height_fraction)

        # Assign relative height fractions#
        for height_idx, height_fraction in enumerate(rel_height_fraction_list):
            if height_idx == len(self._rows) -1:
                break
            for cell_id in self._rows[height_idx]:
                self._set_cell_height_by_id(cell_id, height_fraction)

    def _set_cell_width_fractions(self, image_width: int, max_width: int):
        """
        Does exactly the same for cell widths in each row as the method _set_cell_height_fractions() does
        for each row height. Please read the comment there to understand this method here.
        """
        for row_idx, row in enumerate(self._rows):
            # Width fetching
            width_list: list = []
            for col_idx, cell_id in enumerate(row):
                cell_view = self._views[cell_id]
                width: int = cell_view.get_width()
                width_list.append(width)

            # Absolute fraction computation
            abs_width_fraction_list: list = []
            for width_idx, curr_width in enumerate(width_list):
                abs_width_fraction = curr_width / image_width * (image_width / max_width)
                abs_width_fraction_list.append(abs_width_fraction)

            # Relative fraction computation
            rel_width_fraction_list: list = []
            for width_idx, curr_width in enumerate(abs_width_fraction_list):
                rel_width_fraction = curr_width / sum(abs_width_fraction_list[width_idx:])
                rel_width_fraction_list.append(rel_width_fraction)

            # Assign relative width fractions
            for width_idx, width_fraction in enumerate(rel_width_fraction_list):
                if width_idx == len(row) -1:
                    break
                cell_id = self.get_cell_index_row_column(row_idx, width_idx)
                self._set_cell_width_by_id(cell_id, width_fraction)
