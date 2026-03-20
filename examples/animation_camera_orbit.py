# Example script to animate an orbiting camera around a static case.

from vifpara import Config
from vifpara import ColorMap
from vifpara import Vector3
from vifpara import Visualization3D
from vifpara import CaseType
from vifpara import Case
from vifpara import Exporter
from vifpara import logger
from vifpara import Layout
from vifpara import set_palette, PaletteOption
from vifpara import annotate_time

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    config = Config("config_motorbike.json")

    # Load case
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)
    case.set_mesh_regions(['internalMesh'])

    # Setup layout
    layout = Layout([1])
    layout.set_height(800)

    # Log available mesh regions and field information
    case.log_patch_array_info()
    case.log_cell_arrays()

    # Create color map
    color_map = ColorMap(field='U', preset='Rainbow Uniform')

    # Create 3D visualization
    vis_obj1 = Visualization3D(
        case=case,
        cam_position=Vector3(-25, 31, 11),
        cam_up=Vector3(0, 0, 1),
        focal_point=Vector3(0, 0, 0),
        zoom=1/15)

    annotate_time(vis_obj1)

    # Add case to 3D visualization
    vis_obj1.add_case_or_clip_to_view(case=case, opacity=0.2, color_map=color_map)
    vis_obj1.render(layout)

    # Animate orbiting camera with given radius, start and end time, and the number of frames
    exporter = Exporter(config=config, layout=layout)
    exporter.save_camera_orbit_animation(
        filename="animation_camera_orbit",
        start_time=500,
        end_time=510,
        nr_frames=10,
        framerate=2,
        orbiting_visualization=vis_obj1)
