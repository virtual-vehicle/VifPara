# Example script to create a single slice

from vifpara import Config
from vifpara import Slice, ColorMap, CaseType, Case
from vifpara import Layout, Vector3
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
    case.log_blocknames()

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.log_patch_array_info()
    # get available fields
    case.log_cell_arrays()

    # Define single view layout
    layout = Layout([1])

    # Create color bar
    cmap = ColorMap(field='U', component_title='Magnitude', legend_title='Velocity', preset='Rainbow Uniform')

    cam_up = Vector3.forward()
    cam_up.x = 0.5
    cam_up.y = 0.7

    norm = Vector3.up()
    norm.x = 0.3
    norm.y = 0.8
    # Create slice object
    slice_obj = Slice(
        case=case,
        normal=norm,
        origin=Vector3(0.0, 0.0, 1.1),
        camera_up=cam_up,
        color_map=cmap,
        height=540,
        margin_x=300)

    # Render slice in single view layout
    slice_obj.render(layout)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Save screenshot of slice
    exporter.save_snapshot(filename="single_slice")
