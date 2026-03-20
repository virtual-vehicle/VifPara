# Example script to create a slice matrix with one centered color bar and larger color legend

from vifpara import Config
from vifpara import Slice
from vifpara import ColorMap
from vifpara import CaseType
from vifpara import Case
from vifpara import Layout
from vifpara import Vector3
from vifpara import SliceMatrix
from vifpara import SliceMatrixColorType
from vifpara import Exporter
from vifpara import logger
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

    # Layout with 3 rows
    cell_array = [2, 2, 2]

    # Define layout
    layout = Layout(cell_array=cell_array)

    # Stores all slices
    slices = []

    # Create color map with specified title and lable font size
    color_map = ColorMap(field='U', legend_title='Velocity', legend_font='Arial', title_font_size=35,
                         label_font_size=30)

    # Define slice normals and camera up vector
    normals = [Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0), Vector3(1.0, 0.0, 0.0),
               Vector3(0.0, 1.0, 0.0), Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0)]
    camera_up = Vector3(0.0, 0.0, 1.0)

    # Define height for slices in pixels.
    height_slice = 520

    # Create slice objects and add them to the slice vector.
    for i in range(0, len(normals)):
        slice_obj = Slice(
            case=case,
            normal=normals[i],
            camera_up=camera_up,
            color_map=color_map,
            height=height_slice)
        slices.append(slice_obj)

    # Create slice matrix with specified color bar height
    slice_matrix = SliceMatrix(
        slices,
        color_type=SliceMatrixColorType.COLOR_CENTERED,
        height_slice=height_slice,
        height_color_bar=150)

    # Render slices in slice matrix
    slice_matrix.render(layout)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Store render as png
    exporter.save_snapshot(filename="slice_matrix_larger_color_bar_legend")