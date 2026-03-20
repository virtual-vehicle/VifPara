# Example script to create a slice array through the whole case

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

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.log_patch_array_info()
    # get available fields
    case.log_cell_arrays()

    direction = Vector3.right()
    origin = Vector3(0.0, 0.0, 1.1)

    # Create color bar
    cmap = ColorMap(field='U', component_title='Magnitude', legend_title='Velocity', preset='Rainbow Uniform')

    slice_array = Slice.generate_slice_array(
        case=case,
        generator_direction=direction,
        num_slices=20,
        camera_up=Vector3.forward(),
        color_map=cmap,
        height=540)

    # Iterate through all slices and create a new single slice image for each
    for idx, slice_obj in enumerate(slice_array):
        # Define single view layout
        # In this setup, it is important to have a layout and exporter for each individual slice
        # You can of course also set multiple slices of the slice_array into a single layout in different cells and
        # export it as one image.
        layout = Layout([1, 1])
        # Render slice in single view layout
        slice_obj.set_color_bar_size(height=80)
        slice_obj.render(layout, row=0, col=0)
        slice_obj.render_color_bar(layout, row=1, col=0)

        layout.set_height(800)
        exporter = Exporter(config=config, layout=layout)

        # Save screenshot of slice
        exporter.save_snapshot(filename=f"slice_array_nr_{idx}")