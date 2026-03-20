# Logger

A custom formatted logger, which logs to the stdout and optionally to a timestamped file.
When the logfile reaches a certain size threshold, it is rotated.

### *class* Logger(name, logpath=None)

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
  * **logpath** (*Optional* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – The directory where log files should be stored.
    If `None`, file logging is disabled until a logpath is provided.
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

### restore_stderr()
