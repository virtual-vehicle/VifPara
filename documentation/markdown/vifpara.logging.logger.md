# Logger

A custom formatted logger, which logs to the stdout and optionally to a timestamped file.
When the logfile reaches a certain size threshold, it is rotated.

### *class* Logger

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Initialize a Logger instance with optional file logging.

If you want to use logging, it is advised to not create your own Logger object, but rather use the
global logger object from this module. It is already instantiated, and is automatically configured
with the Config object.

This sets up internal state for:
- log file paths
- rotating file handlers
- stdout handler
- formatting configuration
But the actual logging handlers are only created once initialization is completed later.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The name of the logger.
  * **log_path** (*Optional* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – The directory where log files should be stored.
    If `None`, file logging is disabled until a log_path is provided.
* **Returns:**
  None

#### debug(msg)

Log a debug‑level message.

* **Parameters:**
  **msg** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The message to log.
* **Returns:**
  None

#### info(msg)

Log an info‑level message.

* **Parameters:**
  **msg** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The message to log.
* **Returns:**
  None

#### warning(msg)

Log a warning‑level message.

* **Parameters:**
  **msg** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The message to log.
* **Returns:**
  None

#### error(msg)

Log an error‑level message.

* **Parameters:**
  **msg** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The message to log.
* **Returns:**
  None

#### log_path_is_set()

Checks if the log path in the logger is set.
:return bool: True if there is a log path set.

* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

#### set_log_path(log_path)

Sets the log path to enable the logger to write output into logfiles in the
set directory.

* **Parameters:**
  **log_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The path to put the logfiles.

#### clear_log_path()

Clears the log path, so that the logger does not write into a file anymore.

#### capture_stderr()

Capture all standard error (stderr) output and redirect it into the logger.

This should be called at the beginning of the script.  
Stderr is intercepted at the OS level,
and forwarded to the logger.

* **Returns:**
  None

#### restore_stderr()

Restore stderr to its default behavior.

* **Returns:**
  None
