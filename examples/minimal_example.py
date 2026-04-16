# The minimal example from the get started chapter of the documentation.
# Exports a single slice of a case.

from vifpara import *

if __name__ == "__main__":
    # Read config and load case
    config = Config(custom_config = {"case_path": "data/simpleFoam_motorbike/case.foam",
                                     "plot_path": "plots/motorbike",
                                     "log_path": "logs/motorbike"})
    logger.set_log_path(config.get_log_path())
    case = Case(config=config, loader="openfoam", case_type=CaseType.RECONSTRUCTED)

    # Define single view layout
    layout = Layout([1])

    # Create color map
    cmap = ColorMap(field="U")

    # Create slice object
    slice_obj = Slice(
        case=case,
        color_map=cmap,
        normal=Vector3(0.0, 1.0, 0.0))

    # Render slice in single view layout
    slice_obj.render(layout)
    layout.set_height(800)
    exporter = Exporter(config=config, layout=layout)

    # Save screenshot of slice
    exporter.save_snapshot(filename="minimal_example")