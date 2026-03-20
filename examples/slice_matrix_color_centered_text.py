# Example script to create a slice matrix with centered color bar and text annotations

from vifpara import Config
from vifpara import Slice
from vifpara import ColorMap
from vifpara import CaseType
from vifpara import Case
from vifpara import Layout
from vifpara import Vector3
from vifpara import SliceMatrix
from vifpara import SliceMatrixColorType
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

    # Define layout with 3 rows
    layout = Layout(cell_array=[2, 2, 2])

    # Stores all slices
    slices = []

    # Define text annotations in the first row and column
    text_first_row = ["first column", "second column", "third column"]
    text_first_column = ["first row", "second row", "third row"]

    # Create color map
    color_map = ColorMap(field='U')

    # Define slice normals and camera up vector
    normals = [Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0), Vector3(1.0, 0.0, 0.0),
               Vector3(0.0, 1.0, 0.0), Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0)]
    camera_up = Vector3(0.0, 0.0, 1.0)

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

    # Create the slice matrix with one centered color bar and specified text annotations on the top and left.
    slice_matrix = SliceMatrix(
        slices,
        texts_top=text_first_row,
        texts_left=text_first_column,
        color_type=SliceMatrixColorType.COLOR_CENTERED,
        font='Times',
        font_size=25,
        text_view_height=100,
        height_slice=height_slice)

    # Render slices in slice matrix
    slice_matrix.render(layout)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Store render as png
    exporter.save_snapshot(filename="slice_matrix_color_centered_text")