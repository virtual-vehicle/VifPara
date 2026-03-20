# Example script to visualize slice planes in 3D

from vifpara import Config
from vifpara import Slice
from vifpara import ColorMap
from vifpara import Vector3
from vifpara import Visualization3D
from vifpara import CaseType
from vifpara import Case
from vifpara import Layout
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

    # Get available mesh regions
    case.log_patch_array_info()
    # Get available field options
    case.log_cell_arrays()

    # Stores all slices
    slices = []

    # Define normals and camera up for slices
    normals = [Vector3(1.0, 0.0, 0.0), Vector3(0.0, 1.0, 0.0), Vector3(0.0, 0.0, 1.0)]
    camera_up = [Vector3(0.0, 0.0, 1.0), Vector3(0.0, 0.0, 1.0), Vector3(0.0, 1.0, 0.0)]

    # Create layout with 3 columns and 1 row, to save a screenshot for all slices in one view
    slice_layout = Layout(cell_array=[3])

    # Create color map
    color_map = ColorMap(field='U')

    # Iterate through all slice cells in layout and add slices to layout
    for i in range(0, 3):
        normal = normals[i]

        # Create slice with maximum supported view resolution
        slice_obj = Slice(
            case=case,
            normal=normal,
            camera_up=camera_up[i],
            color_map=color_map,
            height=520)

        # Render slice at specified layout position
        slice_obj.render(layout=slice_layout, row=0, col=i)

        # Store slice
        slices.append(slice_obj)

    slice_layout.set_height(800)
    slice_exporter = Exporter(config=config, layout=slice_layout)
    # Save the slices in a slice matrix as png
    slice_exporter.save_snapshot(filename="slices")

    # Create 3D visualization and visualize case and slices in render_view
    # parameter flip_y_label may be needed when camera up is y-up, and the label is flipped
    # text position can be set with the text_position parameter
    vis_layout = Layout([1])

    vis_obj = Visualization3D(
        case=case,
        cam_position=Vector3(-25, 31, 11),
        cam_up=Vector3(0, 0, 1),
        width=900,
        height=720,
        zoom=0.1)

    # Add case to view
    vis_obj.add_case_or_clip_to_view(case=case, color_map=color_map, opacity=0.2)

    # Add all slices with different text annotations to view
    vis_obj.add_slice_to_view(slice=slices[0], opacity=0.2, text='x = 0', text_scale=0.4)
    vis_obj.add_slice_to_view(slice=slices[1], text='y = 0', text_scale=0.4)
    vis_obj.add_slice_to_view(slice=slices[2], text='z = 0', text_scale=0.4)

    vis_obj.render(vis_layout)

    vis_layout.set_height(800)
    exporter = Exporter(config=config, layout=vis_layout)

    # Save screenshot
    exporter.save_snapshot(filename="slice_planes_3d_visualization")