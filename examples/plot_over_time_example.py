# Example script for plot over line and data export as .csv.

from vifpara import Config, Layout, Exporter
from vifpara import PlotOverTime
from vifpara import Case
from vifpara import CaseType
from vifpara import Vector3
from vifpara import logger
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    # Read config
    config = Config("config_motorbike.json")
    # Set logpath to enable logger to print to a file
    logger.set_log_path(config.get_log_path())

    # Load case
    case = Case(config=config, loader="openfoam", case_type=CaseType.DECOMPOSED)

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.log_patch_array_info()
    # get available fields
    case.log_cell_arrays()

    layout = Layout([1])

    # Create line plot with case, probe point coordinate, and the selected fields
    time_plot = PlotOverTime(case=case,
                             probe_point=Vector3(2.5, 0.0, 1.0),
                             fields=["U", "k"])

    # Render line plot, stores a x-y plot
    time_plot.render(layout=layout)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Export line plot as graph
    exporter.save_snapshot(filename="plot_over_time_example")

    # Export line plot as csv
    time_plot.export_as_csv(config=config, filename=f"plot_over_time_example_data")