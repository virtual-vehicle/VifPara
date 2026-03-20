# Example script to animate particles.

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

    # Read config
    config = Config("config_lagrangian.json")

    # Load case
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)
    case.set_mesh_regions(['internalMesh'])

    # Load case with different mesh region
    config_particles = Config("config_lagrangian.json")
    case_particles = Case(config=config_particles, case_type=CaseType.RECONSTRUCTED)
    case_particles.set_mesh_regions(['lagrangian/kinematicCloud'])

    # Setup layout
    layout = Layout([1])

    # Create color map
    color_map = ColorMap(field='U.gas')

    # Create 3D visualization
    vis_obj1 = Visualization3D(
        case=case,
        cam_position=Vector3(-25, 31, 11),
        cam_up=Vector3(0, 0, 1),
        focal_point=Vector3(0, 0, 0))

    # Add cases to 3D visualization
    vis_obj1.add_case_or_clip_to_view(case=case, opacity=0.2, color_map=color_map)
    vis_obj1.add_case_or_clip_to_view(case=case_particles, color_map=color_map,
                                      representation_type='Point Gaussian', gaussian_radius=0.0012)
    vis_obj1.render(layout)

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Animate and export as video file
    exporter.save_animation(
        filename="animation_particles",
        framerate=1,
        end_frame=10)