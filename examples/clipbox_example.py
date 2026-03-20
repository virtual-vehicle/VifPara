# Example script to create a clip box.

from vifpara import Config
from vifpara import ColorMap
from vifpara import CaseType
from vifpara import Case
from vifpara import Clipbox
from vifpara import Vector3
from vifpara import Visualization3D
from vifpara import logger
from vifpara import Exporter
from vifpara import Layout
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    # Read config
    config = Config("config_motorbike.json")

    # Load case
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)
    layout = Layout([1])

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.log_patch_array_info()
    # Get available field options
    case.log_cell_arrays()

    # Create color map with legend title and text annotations
    color_map = ColorMap(
        field='U',
        component_title='Magnitude',
        legend_title='Velocity',
        text_upper="Clip Box",
        text_right="0",
        text_left="$\\lambda$",
        legend_font='Arial')

    # Create clipbox object and perform clip
    clip_obj = Clipbox(case=case, position=Vector3(-1.0, -2.0, 0.0), length=Vector3(5.0, 4.0, 3.0))

    # Create 3D Visualization
    vis_obj = Visualization3D(
        case=case,
        cam_position=Vector3(-25, 31, 11),
        cam_up=Vector3(0, 0, 1),
        focal_point=Vector3(0, 0, 0),
        width=900,
        height=720,
        zoom=0.2)
    # Add clip to view
    vis_obj.add_case_or_clip_to_view(case=clip_obj, color_map=color_map, opacity=0.5)
    vis_obj.render(layout)
    # Save screenshot
    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)
    exporter.save_snapshot(filename='clipbox_example')