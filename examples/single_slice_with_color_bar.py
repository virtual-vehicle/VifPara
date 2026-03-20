# Example script to create a single slice with a color bar

from vifpara import Config
from vifpara import Slice
from vifpara import ColorMap
from vifpara import CaseType
from vifpara import Case
from vifpara import Layout
from vifpara import Vector3
from vifpara import logger
from vifpara import Exporter
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)
    # Read config
    config = Config("config_motorbike.json")

    # Load case
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.get_patch_array_info()
    # Get available field options
    case.get_cell_arrays()

    # Define 2-rowed layout
    layout = Layout(cell_array=[1, 1])

    # Create color bar
    cmap = ColorMap(field='U', legend_title='Velocity', legend_font='Arial', preset='Rainbow Uniform',
                    legend_format_digits_after=0)

    # Define slice normal and origin
    normal = Vector3.up()
    origin = Vector3(0.0, 0.0, 1.1)

    # Create slice object
    slice_obj = Slice(
        case=case,
        normal=normal,
        origin=origin,
        camera_up=Vector3.forward(),
        color_map=cmap,
        height=540)

    # Render slice at specified layout position (0, 0)
    slice_obj.render(layout=layout, col=0, row=0)
    # Render color bar at specified layout position (0, 1)
    slice_obj.set_color_bar_size(height=80, width=slice_obj.get_width())
    slice_obj.render_color_bar(layout=layout, col=0, row=1)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Save screenshot of slice
    exporter.save_snapshot(filename="single_slice_with_color_bar")