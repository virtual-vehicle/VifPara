"""
A custom formatted logger, which logs to the stdout and optionally to a timestamped file.
When the logfile reaches a certain size threshold, it is rotated.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
from datetime import datetime
from typing import Optional
import threading
import os
import atexit
import time
import colorama


stderr_thread: Optional[int] = None
_stderr_saved_fd: Optional[int] = None


class TextColor:
    DEFAULT = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[33m"
    CYAN = "\033[96m"


class Logger:
    def __init__(self, name: str, logpath: Optional[str] = None):
        """
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

        :param str name: The name of the logger.
        :param Optional[str] logpath: The directory where log files should be stored.
            If ``None``, file logging is disabled until a logpath is provided.
        :return: None
        """
        colorama.init(autoreset=True)

        self.name = name
        self._logpath: Optional[str] = logpath

        self._timestamp = None
        self._initialized: bool = False
        self._logpath_set: bool = False

        self._curr_log_path: Optional[Path] = None
        self._logfile_path: Optional[Path] = None
        self._logger: Optional[logging.Logger] = None
        self._file_handler: Optional[RotatingFileHandler] = None
        self._stdout_handler: Optional[logging.StreamHandler] = None
        self._formatter: Optional[logging.Formatter] = None
    
    def debug(self, msg: str):
        """
        Log a debug‑level message.

        :param str msg: The message to log.
        :return: None
        """
        if not self._initialized:
            self._initialize()
        self._logger.debug(f"{colorama.Fore.CYAN}{msg}")

    def info(self, msg: str):
        """
        Log an info‑level message.

        :param str msg: The message to log.
        :return: None
        """
        if not self._initialized:
            self._initialize()
        self._logger.info(f"{msg}")

    def warning(self, msg: str):
        """
        Log a warning‑level message.

        :param str msg: The message to log.
        :return: None
        """
        if not self._initialized:
            self._initialize()
        self._logger.warning(f"{colorama.Fore.YELLOW}{msg}")

    def error(self, msg: str):
        """
        Log an error‑level message.

        :param str msg: The message to log.
        :return: None
        """
        if not self._initialized:
            self._initialize()
        self._logger.error(f"{colorama.Fore.RED}{msg}")

    def logpath_is_set(self) -> bool:
        return self._logpath_set

    def set_logpath(self, logpath: str):
        if self._logpath_set:
            return

        self._logpath = logpath

        # When the logger is initialized, it can print.
        # When it already is initialized (due to using the logger) but the logpath is set afterward,
        # reinitialize the logger. But then do not allow a new logpath to be set, so we can use multiple
        # configs with the same logfile.
        self._logpath_set = True
        self._initialized = False

    def capture_stderr(self):
        """
        Capture all standard error (stderr) output and redirect it into the logger.

        This should be called at the beginning of the script.  
        Stderr is intercepted at the OS level,
        and forwarded to the logger.

        :return: None
        """
        capture_stderr_os_level(lambda msg: logging_callback(msg))
        # This atexit callback is a small timeframe for error messages to go through the stderr thread
        # before program terminates. Otherwise, the error messages just get cut off.
        atexit.register(atexit_callback)

    def restore_stderr(self):
        """
        Restore stderr to its default behavior.

        :return: None
        """
        restore_stderr()
        atexit.unregister(atexit_callback)

    def _drop_handles(self):
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)
            handler.close()

    def _initialize(self):
        if self._initialized:
            return

        if self._logger is not None:
            self._drop_handles()

        self._initialized = True
        if self._timestamp is None:
            self._timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self._logger = logging.getLogger(self.name)
        self._logger.setLevel(logging.DEBUG)
        self._formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

        # Set stdout logging
        self._stdout_handler = logging.StreamHandler(sys.stdout)
        self._stdout_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._stdout_handler)

        # Set file logging
        if self._logpath is not None:
            self._curr_log_path = Path(self._logpath)
            self._logfile_path = self._curr_log_path / Path(f"{self._timestamp}.log")
            self._curr_log_path.mkdir(parents=True, exist_ok=True)
            self._file_handler = RotatingFileHandler(
                str(self._logfile_path),
                maxBytes=5 * 1024 * 1024,  # 5mb files
                backupCount=10
            )
            self._file_handler.setFormatter(self._formatter)
            self._logger.addHandler(self._file_handler)

        self.info(f"Logging initialized for {sys.argv[0]}.")


def capture_stderr_os_level(callback):
    global stderr_thread, _stderr_saved_fd

    # Save current OS-level stderr (fd 2)
    _stderr_saved_fd = os.dup(2)

    r_fd, w_fd = os.pipe()

    # Redirect process stderr -> pipe
    os.dup2(w_fd, 2)
    os.close(w_fd)

    # Optional: make Python's sys.stderr point at the redirected fd too
    # so Python-level writes also follow the same route.
    sys.stderr = os.fdopen(os.dup(2), "w", buffering=1, encoding="utf-8", errors="replace")

    def reader():
        with os.fdopen(r_fd, "r", encoding="utf-8", errors="replace") as pipe:
            for line in pipe:
                callback(line.rstrip("\n"))

    stderr_thread = threading.Thread(target=reader, daemon=True)
    stderr_thread.start()

def restore_stderr():
    global _stderr_saved_fd
    if _stderr_saved_fd is not None:
        os.dup2(_stderr_saved_fd, 2)
        os.close(_stderr_saved_fd)
        _stderr_saved_fd = None

        # Recreate sys.stderr from the restored fd
        sys.stderr = os.fdopen(os.dup(2), "w", buffering=1, encoding="utf-8", errors="replace")

def logging_callback(message):
    global logger
    split_msg: list = message.split("|", 1)
    if len(split_msg) == 1:
        logger.error(message[:-1])
        return

    prefix = split_msg[0]
    raw_msg = split_msg[1]

    if "paraview" in prefix:
        # We need [:-1] to strip the last character, which is always an additonal newline in this setup.
        if "ERR" in prefix:
            logger.error(raw_msg[:-1])
        elif "WARN" in prefix:
            logger.warning(raw_msg[:-1])
        elif "FATL" in prefix:
            logger.error(raw_msg[:-1])
        else:
            logger.info(raw_msg[:-1])
    else:
        logger.error(message[:-1])

def atexit_callback():
    time.sleep(0.5)
    logger.info("Program finished.")

# Create Singleton with predefined name
logger: Logger = Logger("VifPara")
