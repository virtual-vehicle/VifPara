# Start Your First Script

## Workflow
To use VifPara, you generally follow this workflow in your script. You will find variants of this workflow in all example scripts in the GitHub repository:

1. **Read config** Defines log/plots dir and case path
2. **Load case** Load the case defined in the config
3. **Create layout** Define how many views you want and how they are ordered
4. **Create view objects** Create the objects you want to view and configure them
5. **Attach view modifiers** Create view modifiers and attach them to the view objects (optional step)
6. **Render view objects** Tell the views where you want them to be in your layout
7. **Export image/animation** Save the layout with its views in files

> **Info**
> It is important to understand how size assignment works in VifPara. When you create new views, you always assign a size in pixels to them.
> The layout uses those sizes to understand the relative dimensions of all views to each other. When exporting, the layout uses the height you assigned to it ,
> to compute new sizes which fit into your provided size.

> **Warning**
> The layout resizing feature is primarily here because of a behavior of ParaView. When you try to export a layout which is larger than the screen resolution of your primary display, it can lead to undesired cropping, and incorrect layout display.

## Configuration
To tell your vifpara script where your testcase exists on your system, you need to provide this path to a config object in your VifPara script.

### Set paths in config.json
The config.json needs to look like this:

```json
{
   "case_path": "<path/to/your/case>",
   "plot_path": "<path/to/your/output/image/directory>",
   "log_path":  "<path/to/your/log/file/directory>"
}
```

Use it in your script like so:

```python
config = Config("<path/to/your/config.json>")
```

> **Info**
> If you do not provide a parameter for read_config(), it will look for a config file called config.json in your current working directory.

Alternatively set the config directly in your Python code like so:
```python
config = Config(custom_config = {
                  "case_path": "<path/to/your/case>",
                  "plot_path": "<path/to/your/output/image/directory>",
                  "log_path":  "<path/to/your/log/file/directory>"
               })
```

## Running a First Script

First you need to have VifPara installed in a Python environment using pip, and you need a compatible ParaView versionon your machine.

This example uses the [OpenFoam motorbike testcase](https://develop.openfoam.com/Development/openfoam/-/tree/OpenFOAM-v2412/tutorials/incompressible/simpleFoam/motorBike). Simulate it with OpenFoam. Afterwards, you point the case_path in the config to the case.foam of the testcase. If it does not exist, just create an empty file with this name in the cases root directory.

```python
from vifpara import *

if __name__ == "__main__":
    # 1. Read config
    config = Config(custom_config = {"case_path": "tutorials/incompressible/simpleFoam/motorBike/case.foam",
                                     "plot_path": "plots/motorBike",
                                     "log_path": "logs/motorBike"})
                                     
    # 2. Load case
    case = Case(config=config, case_type=CaseType.RECONSTRUCTED)
    logger.set_log_path(config.get_log_path())

    # 3. Create layout
    layout = Layout([1])

    # 4. Create view objects
    cmap = ColorMap(field="U")
    slice_obj = Slice(
        case=case,
        color_map=cmap,
        normal=Vector3(0.0, 1.0, 0.0))

    # 5. Render view objects
    slice_obj.render(layout, row=0, col=0)
    layout.set_height(800)

    # 6. Export image/animation
    exporter = Exporter(config=config, layout=layout)
    exporter.save_snapshot(filename="motorbike_slice")
```

Save this script as motorbike_slice.py and run it with the following line.

```bash
vifpara motorbike_slice.py
```

The resulting image should look like this.

![Motorbike slice export](motorbike_slice.png)

For more functions and explanations consult the API Reference in this page and visit the example scripts in the GitHub page.