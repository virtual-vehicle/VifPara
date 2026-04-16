# Example script to visualize a pvd file.

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
    config = Config(custom_config = {
        "case_path": "data/filetypes/pvd_testfile.pvd",
        "plot_path": "plots/filetypes",
        "log_path": "logs/filetypes"
    })
    # Set logpath to enable logger to print to a file
    logger.set_log_path(config.get_log_path())

    # Load drop case
    case = Case(config=config, loader="file")
    case.log_blocknames()
    case.log_patch_array_info()
    case.log_cell_arrays()
    case.log_point_arrays()
    layout = Layout([1])

    # Create color maps
    color_map = ColorMap(field='T_pred', preset='Rainbow Uniform')

    # Create 3D visualization object
    vis_obj1 = Visualization3D(
        case=case,
        cam_position=Vector3(3.0, 4.0, 0.0),
        cam_up=Vector3(0, 0.0, 1.0),
        focal_point=Vector3(3.0, -1.0, 0.0),
        zoom=0.3,
        show_orientation_axis=True
    )

    # Add both cases to the 3D view
    vis_obj1.add_case_or_clip_to_view(case, color_map)
    vis_obj1.render(layout)

    # Save a screenshot
    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)
    exporter.save_snapshot(filename="filetype_pvd")