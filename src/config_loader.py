"""
This module contains logic for loading csort configurations from a .ini file.
"""
import configparser
import logging
from pathlib import Path
from typing import Optional

from src.configs import DEFAULT_CONFIG_FILE_NAME
from src.configs import DEFAULT_CSORT_GENERAL_PARAMS
from src.configs import DEFAULT_CSORT_ORDER_PARAMS


class ConfigLoader:
    """
    A class for loading csort configurations from a .ini file

    Attributes:
        _config_path: user defined path to .ini file
        _config_parser: instance of ConfigParser
        _loaded_config: if True, then config has already been loaded

    Methods:
        _locate_config_file: find the .ini file in working directory
        _read_config: read configurations from .ini file
        _load_config: load a configuration file either by finding the file or using user provided path
        config: access the _config_parser attribute
    """

    def __init__(self, config_path: Optional[str] = None) -> None:
        self._config_path = config_path
        self._config_parser = configparser.ConfigParser()
        self._loaded_config: bool = False

    @staticmethod
    def _locate_config_file() -> Optional[str]:
        csort_ini_files = list(Path.cwd().glob(DEFAULT_CONFIG_FILE_NAME))
        if len(csort_ini_files) > 1:
            raise ValueError(f"More than one {DEFAULT_CONFIG_FILE_NAME} file found!")
        if len(csort_ini_files) == 1:
            return csort_ini_files[0].as_posix()
        return None

    def _read_config(self, config_path: str) -> None:
        self._config_parser.read(config_path)
        self._loaded_config = True

    def _load_defaults(self) -> None:
        self._config_parser["csort.order"] = DEFAULT_CSORT_ORDER_PARAMS
        self._config_parser["csort"] = DEFAULT_CSORT_GENERAL_PARAMS

    def _load_config(self) -> None:
        config_path = self._locate_config_file() if self._config_path is None else self._config_path
        if config_path is None:
            logging.warning("No config file found! Using default behaviours.")
            self._load_defaults()
        else:
            self._read_config(config_path)

    @property
    def config(self) -> configparser.ConfigParser:
        if self._loaded_config:
            return self._config_parser
        self._load_config()
        return self._config_parser
