# Example script to save all timesteps of an ensight case into multiple png files.

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

    # Load cases -> set loader to ensight
    case = Case(config=config, loader='ensight')
    layout = Layout([1])

    # Load geometry case (use config path if geo_case_path not specified)
    #geo_case_path = config.get('geo_case_path', config['case_path'])
    case_geo = Case(config=config, loader='ensight')

    # Create color maps
    color_map = ColorMap(field='velocity', preset='Rainbow Uniform')
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

    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Save screenshot of 3D view
    exporter.save_snapshot(filename="ensight_save_at_all_timesteps_snapshot")

    # Save screenshot of 3D view at all available timesteps
    exporter.save_at_all_timesteps(filename='ensight_save_at_all_timesteps')
