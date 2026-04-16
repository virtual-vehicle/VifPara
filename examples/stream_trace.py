# Example script to visualize stream traces.

from vifpara import Config
from vifpara import ColorMap
from vifpara import CaseType
from vifpara import Case
from vifpara import Vector3
from vifpara import Layout
from vifpara import Slice
from vifpara import StreamTracer
from vifpara import logger
from vifpara import Exporter
from vifpara import set_palette, PaletteOption

if __name__ == '__main__':
    logger.capture_stderr()

    set_palette(PaletteOption.WHITE)

    # Read config
    config = Config("config_motorbike.json")
    # Set logpath to enable logger to print to a file
    logger.set_log_path(config.get_log_path())

    # Load case
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)

    # Set mesh regions
    case.set_mesh_regions(['internalMesh'])

    # Get available mesh regions
    case.log_patch_array_info()
    # Get available field options
    case.log_cell_arrays()

    # Define single view layout
    layout = Layout(cell_array=[1])

    # Create color bar
    cmap = ColorMap(field='U', component_title='Magnitude')

    # Define slice normal and origin
    origin = Vector3(5.0, 0.0, 4.0)
    normal = Vector3(0.0, 1.0, 0.0)

    # Create slice object
    slice_obj = Slice(
        case=case,
        normal=normal,
        origin=origin,
        camera_up=Vector3(0.0, 0.0, 1.0),
        color_map=cmap,
        height=540)

    # Create stream trace object upon slice
    stream_obj = StreamTracer(vectors = ("POINTS", "U"),
                              color_array_name = ("POINTS", "k", "Magnitude"),
                              seed_point_1 = Vector3(-4.8360322, 0, -1),
                              seed_point_2 = Vector3(15.123393, -0.027608272, 7.90837163),
                              representation_type = "Surface",
                              max_stream_length = 20.0,
                              resolution = 100)
    # Render and save stream trace visualization
    stream_obj.attach(slice_obj)

    # Perform slice at cell position 0 -> single view
    slice_obj.render(layout)

    exporter = Exporter(config=config, layout=layout)
    exporter.save_snapshot(filename="stream_trace")