# Example script for saving time variant data at all available timesteps

from vifpara import Config
from vifpara import ColorMap
from vifpara import Vector3
from vifpara import CaseType
from vifpara import Case
from vifpara import Layout
from vifpara import Slice
from vifpara import Exporter
from vifpara import logger
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    # Read config
    config = Config("config_motorbike.json")
    # Set logpath to enable logger to print to a file
    logger.set_log_path(config.get_log_path())

    # Load casecd
    case = Case(config=config, loader="openfoam", case_type=CaseType.DECOMPOSED)

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.log_patch_array_info()
    # get available fields
    case.log_cell_arrays()

    # Create color map
    cmap = ColorMap(field='U', component_title='Magnitude', legend_title='Velocity', preset='Rainbow Uniform')

    # Define 2-rowed layout
    layout = Layout([1, 1])
    layout.set_height(800)

    # Create slice object
    slice_obj = Slice(
        case=case,
        normal=Vector3.up(),
        origin=Vector3(0.0, 0.0, 1.1),
        camera_up=Vector3.forward(),
        color_map=cmap,
        height=540)

    # Render slice in first row of layout
    slice_obj.render(layout=layout, row=0, col=0)
    # Render color bar in second row of layout with specified height and width
    slice_obj.set_color_bar_size(height=80, width=slice_obj.get_width())
    slice_obj.render_color_bar(layout=layout, row=1, col=0)

    # Save layout at all available timesteps
    exporter = Exporter(config=config, layout=layout)
    exporter.save_at_timesteps(filename="save_slices_at_timesteps", timesteps=[200, 400, 500])
