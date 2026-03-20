# Exporter

### *class* Exporter(layout, config)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Initialize an exporter responsible for creating images and videos from a layout.

The exporter takes a layout and saves images and animations to the set plots path inside a config instance.

* **Parameters:**
  * **layout** ([*Layout*](vifpara.base.layout.md#vifpara.base.layout.Layout)) – The layout object to export.
  * **config** ([*Config*](vifpara.base.config.md#vifpara.base.config.Config)) – The configuration object containing the output directories
    for saving exported images and videos.
* **Returns:**
  None
* **Raises:**
  [**TypeError**](https://docs.python.org/3/library/exceptions.html#TypeError) – If the provided layout is not a `Layout` instance or the
  config is not a `Config` instance.

#### save_snapshot(filename)

Save a single screenshot of the layout at the first timestep.

* **Parameters:**
  **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The base filename (without extension) for the exported image.
* **Returns:**
  None

#### save_at_timesteps(filename, timesteps)

Save the layout as PNG images at the specified timesteps.

This behaves like `save_animation` in image mode (e.g., PNG export),
but uses explicit timestep values rather than frame indices.

* **Parameters:**
  * **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The base filename (without extension) for exported images.
  * **timesteps** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *]*) – The list of timesteps at which images should be saved.
* **Returns:**
  None

#### save_at_all_timesteps(filename)

Save the layout as PNG images at all available timesteps.

This behaves like `save_animation` in image mode (PNG export),
but saves frames at actual timestep values instead of frame indices.

* **Parameters:**
  **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The base filename (without extension) for exported images.
* **Returns:**
  None

#### save_animation(filename, start_frame=0, end_frame=-1, framerate=30, format='.ogv')

Save an animation of the layout.

This method exports either a video (e.g., `.ogv`) or a sequence of image frames
(e.g., `.png` or `.jpg`), depending on the file extension provided.

* **Parameters:**
  * **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The base filename (without extension) for the animation export.
  * **start_frame** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The index of the first frame to render (must be ≥ 0).
  * **end_frame** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The index of the last frame to render. If `-1` or greater than
    the number of frames, it is automatically clamped to the maximum available frame.
  * **framerate** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The framerate of the exported video.
  * **format** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The output format (e.g., `".png"`, `".jpg"`, `".jpeg"`, `".ogv"`).
* **Returns:**
  None

#### save_camera_orbit_animation(orbiting_visualization, filename, start_time, end_time, nr_frames, framerate, format='.ogv')

Save an animation of a camera orbiting around a focal point in a 3D visualization.

This creates a camera animation path (orbit) and renders frames along the path.
The output can be an image sequence or a video depending on the file extension.

* **Parameters:**
  * **orbiting_visualization** ([*Visualization3D*](vifpara.views.visualization_3D.md#vifpara.views.visualization_3D.Visualization3D)) – The 3D visualization whose camera should orbit.
  * **filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The base filename (without extension) for the exported animation.
  * **start_time** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The starting timestep of the animation.
  * **end_time** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The ending timestep of the animation.
  * **nr_frames** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The number of frames to generate between the start and end time.
  * **framerate** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The framerate for exported video formats.
  * **format** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The output format (e.g. `".png"`, `".jpg"`, `".ogv"`).
* **Returns:**
  None
