# Example script to visualize glyphs.

from vifpara import Config
from vifpara import ColorMap
from vifpara import CaseType
from vifpara import Case
from vifpara import Vector3
from vifpara import Layout
from vifpara import Slice
from vifpara import Glyph
from vifpara import logger
from vifpara import Exporter
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    # Read config
    config = Config("config_lagrangian.json")
    # Set logpath to enable logger to print to a file
    logger.set_log_path(config.get_log_path())

    # Load case
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.log_patch_array_info()
    # Get available field options
    case.log_cell_arrays()

    # Define single view layout
    layout = Layout(cell_array=[1])

    # Create color bar
    cmap = ColorMap(field='U', component_title='Magnitude')

    # Define slice normal and origin
    normal = Vector3.forward()
    origin = Vector3(0.0, 0.0, 0.15)

    # Create slice object
    slice_obj = Slice(
        case=case,
        normal=normal,
        origin=origin,
        camera_up=Vector3.up(),
        color_map=cmap,
        height=540)

    # Create glyph object upon slice
    glyph_obj = Glyph()
    # Render and save glyphs visualization
    glyph_obj.attach(slice_obj)

    # Perform slice at cell position 0 -> single view
    slice_obj.render(layout)

    exporter = Exporter(config=config, layout=layout)
    exporter.save_snapshot(filename="glyphs")