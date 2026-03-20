# What is VifPara?

VifPara is an automation framework for [ParaView](https://www.paraview.org/) post processing and visualization. It enables batch processing of cases with a straight-forward syntax. It exists to enable automation of large amounts of post-processing steps with possibly multiple cases. VifPara is fully script-driven, which means that it cannot and is not supposed to replace a detailed, manual post-processing workflow of single cases with a graphical user interface.

## Architecture

VifPara lives inside an arbitrary Python virtual environment, where it is installed into with `pip`. Because ParaView (as the visualization backend) comes with its own baked-in Python environment (`pvpython`), the VifPara venv needs to be connected to the pvpython environment. This connection is automatically handled for you inside a dedicated `vifpara` runner, which is installed together with the VifPara package. This means when running a VifPara script, call it with `vifpara` instead of `python` or `python3`. This causes the VifPara venv to be integrated into the baked-in environment of the `pvpython` executable for the duration of the script.

![VifPara Architecture](vifpara-architecture.png)

## View and View Modifiers

VifPara utilizes ParaView filters, such as Slices, 3D Visualizations, Glyphs, etc. and groups them into building blocks for a visualization strategy.

There are 2 major types of building blocks: Views and View Modifiers.

A view is a a basic filter to structurally visualize a case inside of a cell in your visualization layout. This can be a Slice or a 3D Visualization. View modifers, such as Streamlines, Glyphs, Annotations can then be assigned to the views to display data on top of the base view.
