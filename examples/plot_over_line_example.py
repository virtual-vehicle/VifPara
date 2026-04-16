# Example script for plot over line and data export as .csv.

from vifpara import Config, Layout, Exporter
from vifpara import PlotOverLine
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

    # Create line plot with case, start point, end point, and the selected fields
    vector_magnitude = 4.0
    line_plot = PlotOverLine(case=case,
                             start_point=Vector3(-vector_magnitude, -vector_magnitude, -vector_magnitude),
                             end_point=Vector3(vector_magnitude, vector_magnitude, vector_magnitude),
                             fields=["U", "p"])

    # Render line plot, stores a x-y plot
    line_plot.render(layout=layout)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Export line plot as graph over all timesteps
    timesteps = [100, 200, 300, 400, 500]
    exporter.save_at_timesteps(filename="plot_over_line_example", timesteps=timesteps)

    # Export line plot as csv over all timesteps
    for timestep in timesteps:
        line_plot.export_as_csv(config=config, filename=f"plot_over_line_example_data_{timestep}", timestep=timestep,
                                show_timestep=True)