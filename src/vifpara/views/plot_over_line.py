import os
from typing import List
import paraview.simple as pv

from ..logging import logger
from ..other import Vector3
from ..base import Case, Layout, Config
from . import IViewObject


class PlotOverLine(IViewObject):
    def __init__(self, case: Case, start_point: Vector3, end_point: Vector3, fields: List[str],
                 height: int = 135):
        """
        Initialize a PlotOverLine view for sampling scalar fields along a line and rendering
        an XY chart representation.

        The PlotOverLine view element, can be used to render a line chart, which represents a
        scalar field over a certain, defined line inside your case.
        You can then show this chart in a cell of your layout.
        It also has the additional capability to export its data in a csv file.

        This class enables:
          - Sampling multiple scalar fields along a line in 3D space.
          - Rendering the sampled data in a ParaView XY chart.
          - Exporting the underlying sampled values as CSV.

        :param Case case: The case from which field data is extracted.
        :param Vector3 start_point: The start point of the sampling line.
        :param Vector3 end_point: The end point of the sampling line.
        :param list[str] fields: The scalar field names to extract and plot.
        :param int height: The height of the view representation inside the layout.
        :return: None
        """
        super().__init__(case, 263, height, False)
        self._case = case
        self._start_point = start_point
        self._end_point = end_point
        self._fields: List[str] = fields
        self._render_fields: List[str] = self._unpack_vector_field_names(self._fields)
        self._plot_over_line_obj = pv.PlotOverLine(registrationName='PlotOverLine1', Input=self._case.get_case())
        self._plot_over_line_obj.Point1 = self._start_point.to_list()
        self._plot_over_line_obj.Point2 = self._end_point.to_list()
        self._render_view = pv.CreateView('XYChartView')
        self._display = pv.Show(self._plot_over_line_obj, self._render_view, 'XYChartRepresentation')
        self._display.SeriesVisibility = self._render_fields

    def get_render_object(self):
        """
        Get the underlying ParaView PlotOverLine object.

        :return: The internal PlotOverLine filter used for sampling along the line.
        :rtype: pv.PlotOverLine
        """
        return self._plot_over_line_obj

    def export_as_csv(self, config: Config, filename: str, timestep: float = 0.0, show_timestep: bool = True):
        """
        Export the sampled scalar field data along the line to a CSV file.

        The output is written into the plots directory defined by the provided ``Config`` object.
        The underlying pipeline is re‑evaluated at the specified timestep before export.

        :param Config config: The configuration object providing the output directory.
        :param str filename: The output filename without the ``.csv`` extension.
        :param float timestep: The timestep from which data should be sampled.
        :param bool show_timestep: If ``True``, additional columns with the timestep
            information are added to the exported CSV.
        :return: None
        """
        full_path: str = config.get_plot_path() + filename + ".csv"
        logger.info(f"Saving plot to file {full_path}.")

        animation_scene = pv.GetAnimationScene()
        prev_timestep: float = animation_scene.AnimationTime
        animation_scene.AnimationTime = timestep

        # Updating is important, otherwise the data does not change for csv exports
        pv.UpdatePipeline(time=timestep, proxy=self._plot_over_line_obj)

        fields = self._fields.copy()
        fields.append("arc_length")
        pv.SaveData(
            full_path,
            proxy=self._plot_over_line_obj,
            ChooseArraysToWrite=1,
            PointDataArrays=fields,
            AddTimeStep=show_timestep,
            AddTime=show_timestep,
            AddMetaData=0
        )

        animation_scene.AnimationTime = prev_timestep
        pv.UpdatePipeline(time=prev_timestep, proxy=self._plot_over_line_obj)

    def _unpack_vector_field_names(self, raw_fields: List[str]) -> List[str]:
        proc_fields: List[str] = []

        for arr_name in raw_fields:
            arr = self._case.get_case().CellData[arr_name]
            num_components = arr.GetNumberOfComponents()

            # Automatically generate component names if it’s a vector
            if num_components > 1:
                selected_axes: List[str] = ["X", "Y", "Z", "W"][:num_components]
                unpacked_names = [f"{arr_name}_{axis}" for axis in selected_axes]
                proc_fields += unpacked_names
            else:
                proc_fields.append(arr_name)

        return proc_fields

    def _render_inside(self, layout: Layout, row: int=0, col: int=0):
        logger.info(f"Rendering plot over line to <{row}|{col}>.")
        layout.add_render_view(row, col, self)