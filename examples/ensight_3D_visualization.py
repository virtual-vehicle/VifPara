# Example script to visualize an ensight case in a 3D view.

from vifpara import Config
from vifpara import ColorMap
from vifpara import Vector3
from vifpara import Visualization3D
from vifpara import CaseType
from vifpara import Case
from vifpara import Layout
from vifpara import logger
from vifpara import Exporter
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    # Read config
    config = Config("config_ensight.json")
    # Set logpath to enable logger to print to a file
    logger.set_log_path(config.get_log_path())

    # Load drop case
    case = Case(config=config, loader='ensight')
    layout = Layout([1])

    # Load geometry case (using a default path if not specified)
    #geo_case_path = config.get('geo_case_path', config['case_path'])
    case_geo = Case(config=config, loader='ensight')

    # Create color maps
    color_map = ColorMap(field='velocity', preset='Rainbow Uniform')
    color_map_geo = ColorMap(field='iBE', preset='Rainbow Uniform')

    # Create 3D visualization object
    vis_obj1 = Visualization3D(
        case=case,
        cam_position=Vector3(0.01813, 4.2639e-05, 0.0962979),
        cam_up=Vector3(0, 1.0, 0),
        focal_point=Vector3(0.01813, 4.2639e-05, 0.00286787)
    )

    # Add both cases to the 3D view
    vis_obj1.add_case_or_clip_to_view(case, color_map)
    vis_obj1.add_case_or_clip_to_view(case_geo, color_map_geo, field_type='Cells')
    vis_obj1.render(layout)

    # Save a screenshot
    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)
    exporter.save_snapshot(filename="ensight_3D_visualization")