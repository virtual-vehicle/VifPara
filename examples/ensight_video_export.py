# Example script to save an ogv animation of all timesteps of an ensight case.

from vifpara import Config
from vifpara import ColorMap
from vifpara import Vector3
from vifpara import Visualization3D
from vifpara import CaseType
from vifpara import Case
from vifpara import Exporter
from vifpara import Layout
from vifpara import logger
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    # Read config
    config = Config("config_ensight.json")

    # Load cases, set loader to 'ensight'
    case = Case(config=config, loader='ensight')
    # Optionally, set geo_case_path from config or use a default
    #geo_case_path = config.get('geo_case_path', config['case_path'])
    case_geo = Case(config=config, loader='ensight')
    layout = Layout([1])

    # Create color maps
    color_map = ColorMap(field='temperature', preset='Rainbow Uniform')
    color_map_geo = ColorMap(field='iBE', preset='Rainbow Uniform')

    # Create 3D view
    vis_obj1 = Visualization3D(
        case=case,
        cam_position=Vector3(0.018130223732441664, 4.263920709490776e-05, 0.09629790063177401),
        cam_up=Vector3(0, 1.0, 0),
        focal_point=Vector3(0.018130223732441664, 4.263920709490776e-05, 0.0028678723610937595))

    # Add cases to 3D view, for the geometry case set the field type to 'Cells'
    vis_obj1.add_case_or_clip_to_view(case, color_map)
    vis_obj1.add_case_or_clip_to_view(case_geo, color_map_geo, field_type='Cells')
    vis_obj1.render(layout)

    exporter = Exporter(config=config, layout=layout)

    # Save screenshot of 3D view
    exporter.save_snapshot(filename="ensight_video_export_snapshot")

    # Animate data and export as video file
    exporter.save_animation(filename="ensight_video_export", framerate=10, end_frame=5)