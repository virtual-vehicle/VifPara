# Config

### *class* Config(conf_filename='./config.json', custom_config=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Initialize and load the configuration used by cases and exporters.

The config reads a json from a file or in-line which contains paths to the case to load,
the plots directory, and the logs directory. It is passed later directly to different other
modules to use its information.

You can modify the paths in runtime by using the dedicated setter methods.

If `custom_config` is provided, it overrides any file-based configuration
and `conf_filename` is ignored.

A config must always be a dictionary with the following format and fields:
{

> “case_path”: “path/to/the/input/case/directory/or/file”,
> “dir_plots”: “path/to/the/output/plot/directory”,
> “dir_logs”: “path/to/the/output/logs/directory”

}

* **Parameters:**
  * **conf_filename** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Path to the JSON configuration file to load.
  * **custom_config** (*Optional* *[*[*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *]*) – A configuration dictionary provided inline.
    If set, no file is read and this dictionary becomes the active config.
* **Returns:**
  None

#### set_other_field(field, value)

Set a custom field in the configuration dictionary.

* **Parameters:**
  * **field** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The name of the field to set.
  * **value** – The value to assign to the field.
* **Returns:**
  None

#### set_case_path(new_path)

Set the case path in the configuration.

* **Parameters:**
  **new_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The new path to the case directory.
* **Returns:**
  None

#### set_dir_plots(new_path)

Set the directory where plots should be written.

* **Parameters:**
  **new_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The new path to the plots directory.
* **Returns:**
  None

#### set_dir_logs(new_path)

Set the directory where logs should be stored.

* **Parameters:**
  **new_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The new path to the logs directory.
* **Returns:**
  None

#### get_config()

Get the full configuration dictionary.

* **Return dict:**
  The active configuration as a Python dictionary.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)

#### get_other_field(field)

Get the value of a custom configuration field, if it exists.

* **Parameters:**
  **field** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The name of the field to retrieve.
* **Returns:**
  The value of the field if present, otherwise `None`.

#### get_casepath()

Get the configured case path.

* **Return str:**
  The path to the case directory.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_dir_plots()

Get the directory where plots are stored.

* **Return str:**
  The path to the plots directory.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### get_dir_logs()

Get the directory where logs are stored.

* **Return str:**
  The path to the logs directory.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

#### dir_logs_is_set()

Check whether a logs directory is defined in the configuration.

* **Return bool:**
  `True` if a logs directory is set, otherwise `False`.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### get_filename()

Get the filename of the loaded configuration file.

* **Return str:**
  The configuration file name.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)
