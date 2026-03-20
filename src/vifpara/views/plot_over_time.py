import os
from typing import List
import paraview.simple as pv

from ..logging import logger
from ..other import Vector3
from ..base import Case, Layout, Config
from . import IViewObject


class PlotOverTime(IViewObject):
    def __init__(self, case: Case, probe_point: Vector3, fields: list[str] = [], height: int = 135):
        """
        Initialize a PlotOverTime view for sampling scalar fields at a single point and
        rendering an XY chart representation over a time sequence.

        The PlotOverTime view element can be used to display how scalar fields evolve
        over time at a specific point probe location inside your case. You can embed this
        chart into a layout cell, and you can also export the underlying sampled values
        as a CSV file.

        This class enables:
        - Sampling multiple scalar fields at a specific point in 3D space.
        - Rendering the sampled temporal data in a ParaView XY chart.
        - Exporting the underlying sampled values as CSV.

        :param Case case: The evaluated case from which the field data is extracted.
        :param Vector3 probe_point: The point in space at which scalar fields are sampled.
        :param list[str] fields: The scalar field names to extract and plot over time.
        :param int height: The height of the view representation inside the layout.
        :return: None
        """
        super().__init__(case, 263, height, False)
        self._case = case
        self._probe_point = probe_point
        self._fields: List[str] = fields
        self._render_fields: List[str] = fields

        self._case.get_case().UpdatePipeline()

        # Convert cell data to point data to make probing/interpolation reliable.
        self._c2p = pv.CellDatatoPointData(Input=self._case.get_case())
        self._c2p.PassCellData = 1

        # ProbeLocation samples/interpolates arrays at an arbitrary 3D coordinate.
        self._probe = pv.ProbeLocation(registrationName='ProbeLocation1', Input=self._c2p)
        self._probe.ProbeType.Center = self._probe_point.to_list()

        # PlotDataOverTime produces an XY table of probed values across time steps.
        self._plot_over_time_obj = pv.PlotDataOverTime(registrationName='PlotOverTime1', Input=self._probe)

        self._render_view = pv.CreateView('XYChartView')
        self._display = pv.Show(self._plot_over_time_obj, self._render_view, 'XYChartRepresentation')

        visible_series: list = self._generate_visible_series()
        self._display.SeriesVisibility = visible_series
        self._fields = visible_series

    def _generate_visible_series(self) -> list:
        visible_series: list = []
        for series in self._display.SeriesVisibility:
            # max, avg, min, ... are all the same since we probe only a 1d point.
            if "avg(" in series:
                series_allowed: bool = self._check_series_allowed(series)
                if series_allowed:
                    visible_series.append(series)

        return visible_series

    def _check_series_allowed(self, series_name: str) -> bool:
        if len(self._render_fields) == 0:
            return True

        for field in self._fields:
            if f"({field} " in series_name or f"({field})" in series_name:
                return True

        return False

    def _render_inside(self, layout: Layout, row: int=0, col: int=0):
        logger.info(f"Rendering plot over time to <{row}|{col}>.")
        layout.add_render_view(row, col, self)

    def get_render_object(self):
        return self._plot_over_time_obj

    def export_as_csv(self, config: Config, filename: str):
        full_path: str = config.get_dir_plots() + filename + ".csv"
        logger.info(f"Saving plot to file {full_path}.")

        fields = self._fields.copy()
        pv.SaveData(full_path, proxy=self._plot_over_time_obj, ChooseArraysToWrite=1,
                    PointDataArrays=fields, AddMetaData=0)
