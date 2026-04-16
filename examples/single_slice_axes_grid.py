# Example script to create a single slice with an axes grid

from vifpara import Config
from vifpara import Slice
from vifpara import ColorMap
from vifpara import CaseType
from vifpara import Case
from vifpara import Layout
from vifpara import Vector3
from vifpara import AxesGrid
from vifpara import logger
from vifpara import Exporter
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)
    # Read config
    config = Config("config_motorbike.json")
    # Set logpath to enable logger to print to a file
    logger.set_log_path(config.get_log_path())

    # Load case
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.log_patch_array_info()
    # get available fields
    case.log_cell_arrays()

    # Define single view layout
    layout = Layout(cell_array=[1])

    # Create color bar
    cmap = ColorMap(field='U', component_title='Magnitude')

    # Define slice normal and origin
    normal = Vector3.up()
    origin = Vector3(0.0, 0.0, 1.1)

    # Create Axes grid object
    axes_grid_obj = AxesGrid(
        x_title="Custom X",
        y_title="Custom Y",
        z_title="Custom Z",
        title_font_size=20,
        font='Times',
        label_font_size=16)

    # Create slice object with an added axes grid
    slice_obj = Slice(
        case=case,
        normal=normal,
        origin=origin,
        camera_up=Vector3.forward(),
        color_map=cmap,
        height=540)

    # Attach the axes grid object to the slice object.
    axes_grid_obj.attach(slice_obj)

    # Render slice in single view layout
    slice_obj.render(layout)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Save screenshot of slice
    exporter.save_snapshot(filename="single_slice_axes_grid")