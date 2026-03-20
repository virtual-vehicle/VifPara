# Example script to export ogv animation of time variant data.

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

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    config = Config("config_lagrangian.json")

    # Load Case
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)
    case.set_mesh_regions(['internalMesh'])

    # Setup Layout
    layout = Layout([1])
    layout.set_height(800)

    # Create color map
    color_map = ColorMap(field='U', preset='Rainbow Uniform')

    # Create 3D visualization
    vis_obj1 = Visualization3D(
        case=case,
        cam_position=Vector3(-25, 31, 11),
        cam_up=Vector3(0, 0, 1),
        focal_point=Vector3(0, 0, 0))

    # Add case to 3D visualization
    vis_obj1.add_case_or_clip_to_view(case=case, color_map=color_map)
    vis_obj1.render(layout)

    # Animate data and export as video file
    exporter = Exporter(layout=layout, config=config)
    exporter.save_animation(
        filename="animate_time_variant_data",
        framerate=10,
        end_frame=30)
