import json
import os
import sys
from ..logging import logger
from typing import Optional


class Config:
    def __init__(self, conf_filename: str = "./config.json", custom_config: Optional[dict] = None):
        """
        Initialize and load the configuration used by cases and exporters.

        The config reads a json from a file or in-line which contains paths to the case to load,
        the plots directory, and the logs directory. It is passed later directly to different other
        modules to use its information.

        You can modify the paths in runtime by using the dedicated setter methods.

        If ``custom_config`` is provided, it overrides any file-based configuration
        and ``conf_filename`` is ignored.

        A config must always be a dictionary with the following format and fields:
        {
           "case_path": "path/to/the/input/case/directory/or/file",
           "plot_path": "path/to/the/output/plot/directory",
           "log_path": "path/to/the/output/logs/directory"
        }

        :param str conf_filename: Path to the JSON configuration file to load.
        :param Optional[dict] custom_config: A configuration dictionary provided inline.
            If set, no file is read and this dictionary becomes the active config.
        :return: None
        """
        if custom_config is None:
            self.conf_filename: str = conf_filename
            self.config: dict = self._read_config(self.conf_filename)
        else:
            self.conf_filename = ""
            self.config = custom_config

        self._check_config(self.config)

        logger.info(f"Using case path: {self.get_case_path()}")
        logger.info(f"Using plots directory: {self.get_plot_path()}")

    def set_other_field(self, field: str, value):
        """
        Set a custom field in the configuration dictionary.

        :param str field: The name of the field to set.
        :param value: The value to assign to the field.
        :return: None
        """
        self.config[field] = value

    def set_case_path(self, new_path: str):
        """
        Set the case path in the configuration.

        :param str new_path: The new path to the case directory.
        :return: None
        """
        self.config["case_path"] = new_path

    def set_plot_path(self, new_path: str):
        """
        Set the directory where plots should be written.

        :param str new_path: The new path to the plots directory.
        :return: None
        """
        self.config["plot_path"] = new_path

    def set_log_path(self, new_path: str):
        """
        Set the directory where logs should be stored.

        :param str new_path: The new path to the logs directory.
        :return: None
        """
        self.config["log_path"] = new_path

    def get_config(self) -> dict:
        """
        Get the full configuration dictionary.

        :return dict: The active configuration as a Python dictionary.
        """
        return self.config

    def get_other_field(self, field: str):
        """
        Get the value of a custom configuration field, if it exists.

        :param str field: The name of the field to retrieve.
        :return: The value of the field if present, otherwise ``None``.
        """
        if field in self.config:
            return self.config[field]
        else:
            return None

    def get_case_path(self) -> str:
        """
        Get the configured case path.

        :return str: The path to the case directory.
        """
        return self.config["case_path"]

    def get_plot_path(self) -> str:
        """
        Get the directory where plots are stored.

        :return str: The path to the plots directory.
        """
        return self.config["plot_path"]

    def get_log_path(self) -> str:
        """
        Get the directory where logs are stored.

        :return str: The path to the logs directory.
        """
        return self.config["log_path"]

    def log_path_is_set(self) -> bool:
        """
        Check whether a logs directory is defined in the configuration.

        :return bool: ``True`` if a logs directory is set, otherwise ``False``.
        """
        return "log_path" in self.config

    def get_filename(self) -> str:
        """
        Get the filename of the loaded configuration file.

        :return str: The configuration file name.
        """
        return self.conf_filename
    
    def _create_config(self, conf_filename: str = "./config.json"):
        """
        Create a default configuration file.

        This writes a JSON file containing default values for:
        - ``case_path``
        - ``plot_path``
        - ``log_path``

        :param str conf_filename: The filename (including path) where the default
            configuration should be written.
        :return: None
        """
        # Data to be written
        dictionary = {
            "case_path": "./case.foam",
            "plot_path": "./plots/",
            "log_path": "./logs/"
        }
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)

        # Writing to config.json
        with open(conf_filename, "w") as outfile:
            outfile.write(json_object)

    def _read_config(self, conf_filename: str = "./config.json") -> dict:
        """
        Read a configuration file in JSON format.

        If the file does not exist, a default configuration file is created,
        and an ``OSError`` is raised to indicate that initialization must be retried.

        :param str conf_filename: The path to the configuration file to read.
        :return dict: The loaded configuration as a dictionary.
        :raises OSError: If the configuration file does not exist and a default one is created.
        """
        # check if config exists
        config_exists = os.path.isfile(conf_filename)
        if config_exists:
            f = open(conf_filename)
            data = json.load(f)
            f.close()
            return data
        else:
            self._create_config(conf_filename)
            raise OSError("No config.json found in base directory, creating a default config.json file.")

    def _check_config(self, config: dict):
        """
        Validate the configuration dictionary and ensure all required paths exist.

        This method performs the following:
        - Ensures ``case_path`` exists and is valid.
        - Ensures ``plot_path`` ends with a slash and the directory exists (creates it if necessary).
        - Ensures ``log_path`` ends with a slash and the directory exists (creates it if necessary).
        - Raises exceptions when required keys are missing or invalid.

        :param dict config: The configuration dictionary to validate and normalize.
        :return: None
        :raises KeyError: If required keys (``case_path``, ``plot_path``) are missing.
        :raises OSError: If ``case_path`` is set but does not exist.
        """
        # Check case path
        if "case_path" in config:
            if config["plot_path"][-1] != "/":
                config["plot_path"] = f"{config['plot_path']}/"
            case_exists = os.path.exists(config["case_path"])
            if not case_exists:
                raise OSError(f"Case path in config invalid ({config['case_path']})")
        else:
            raise KeyError("Missing 'case_path' in config.")

        # Check plots directory
        if "plot_path" in config:
            if config["plot_path"][-1] != "/":
                config["plot_path"] = f"{config['plot_path']}/"
            plots_dir_exists = os.path.exists(config["plot_path"])
            if not plots_dir_exists:
                logger.info("Plots directory not existing. Creating directory now.")
                os.makedirs(config["plot_path"])
        else:
            raise KeyError("Missing 'plot_path' in config.")
