# Example script to create a slice matrix with color bar for each column and text annotations

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

    # Define text annotations
    text_first_row = ["first column", "second column", "third column"]
    text_first_column = ["first row", "second row", "third row"]

    # Create color map
    color_maps = [ColorMap(field='U', preset='Rainbow Uniform'), ColorMap(field='U', preset='Rainbow Uniform')]

    # Define slice normals and camera up vector
    normals = [Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0), Vector3(1.0, 0.0, 0.0),
               Vector3(0.0, 1.0, 0.0), Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0)]
    camera_up = Vector3(0.0, 0.0, 1.0)

    # Define height of slices in pixels
    height_slice = 520

    # iterate through slice rows, as we have one color bar row and one text annotation row, iterate only through number
    # of rows - 2
    for r in range(0, len(cell_array)):
        # iterate through columns -> skip text annotation column
        for c in range(0, cell_array[0]):
            slice_obj = Slice(
                case=case,
                normal=normals[r*cell_array[0] + c],
                camera_up=camera_up,
                color_map=color_maps[c],
                height=height_slice)
            slices.append(slice_obj)

    # Create slice matrix with color bars for each column and text annotation on the top and left
    slice_matrix = SliceMatrix(
        slices,
        texts_top=text_first_row,
        texts_left=text_first_column,
        color_type=SliceMatrixColorType.COLOR_PER_COLUMN,
        height_slice=height_slice)

    # Render slices in slice matrix
    slice_matrix.render(layout)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Store render as png
    exporter.save_snapshot(filename="slice_matrix_color_per_column_text")