"""
This module contains logic for loading csort configurations from a config file.
"""
import configparser
import logging
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

import toml

from src.configs import DEFAULT_CONFIG_INI_FILE_NAME
from src.configs import DEFAULT_CONFIG_TOML_FILE_NAME
from src.configs import DEFAULT_CSORT_GENERAL_PARAMS
from src.configs import DEFAULT_CSORT_ORDER_PARAMS
from src.configs import DEFAULT_CSORT_ORDERING_SECTION
from src.configs import DEFAULT_CSORT_ORDERING_SUBSECTION
from src.configs import DEFAULT_CSORT_PARAMS_SECTION
from src.configs import Readable


class ConfigLoader(ABC):
    """
    A class for loading csort configurations from a config file

    Attributes:
        _config_path: user defined path to .ini file
        _config_parser: instance of a Readable class
        _loaded_config: if True, then config has already been loaded
        _config: config mapping populated after config file has been loaded

    Methods:
        _locate_config_file: find the config file in working directory
        _read_config: read configurations from .ini file
        _load_config: load a configuration file either by finding the file or using user provided path
        config: access the _config_parser attribute
    """

    default_config_file_name = ""  # this is the file the config loader will look for by default

    def __init__(self, config_path: Optional[str] = None) -> None:
        """
        Initialise the config loader
        Args:
            config_path: path to config file
        """
        self._config_path = config_path
        self._config_parser = self._set_config_parser()
        self._loaded_config: bool = False
        self._config: Optional[Dict[str, Any]] = None

    def _locate_config_file(self) -> List[Path]:
        """
        Find the default config file in local working directory
        Returns:
            list of paths to matching file paths
        """
        return list(Path.cwd().glob(self.default_config_file_name))

    def _validate_config_path(self, config_path: List[Path]) -> Optional[str]:
        """
        Validate that the config loader has found only one possible config file
        Args:
            config_path: list of matching config paths

        Returns:
            config path if only one found, None if no matches

        Raises:
            ValueError: if more than one matching config file found
        """
        if len(config_path) > 1:
            raise ValueError(f"More than one {self.default_config_file_name} file found!")
        if len(config_path) == 1:
            return config_path[0].as_posix()
        return None

    def get_config_file_path(self) -> Optional[str]:
        """
        Wrapper around finding and validating config file paths
        Returns:
            a config file path if a config file is found, else None
        """
        config_files = self._locate_config_file()
        return self._validate_config_path(config_files)

    @abstractmethod
    def _set_config_parser(self) -> Readable:
        """
        Concrete classes implement this method to instantiate a class which reads from the config file
        Returns:
            an instance which meets the Readable protocol
        """
        pass

    @abstractmethod
    def _read_config(self, config_path: str) -> Dict[str, Any]:
        """
        Concrete classes implement this method to load configurations from a config file and perform reformatting.
        Args:
            config_path: path to config file

        Returns:
            a mapping of configurations
        """
        pass

    @staticmethod
    def _load_defaults() -> Dict[str, Any]:
        """
        If no file path is provided or found for csort, then default configurations are loaded
        Returns:
            cfg: mapping of default configurations
        """
        cfg = {"csort.order": DEFAULT_CSORT_ORDER_PARAMS, "csort": DEFAULT_CSORT_GENERAL_PARAMS}
        return cfg

    def _load_config(self) -> Dict[str, Any]:
        """
        Wrapper function for getting the config file path and loading configurations from the file
        Returns:
            cfg: mapping of configurations
        """
        config_path = self.get_config_file_path() if self._config_path is None else self._config_path
        if config_path is None:
            logging.warning("No config file found! Using default behaviours.")
            cfg = self._load_defaults()
        else:
            cfg = self._read_config(config_path)
        self._config = cfg
        return cfg

    @property
    def config(self) -> Dict[str, Any]:
        """
        Property method used to access _config if already loaded. If not loaded, then _load_config is called.
        Returns:
            cfg: mapping of configurations
        """
        if self._loaded_config and self._config is not None:
            return self._config
        cfg = self._load_config()
        return cfg


class IniReader:
    """
    A class for reading configurations from a .ini file into a dictionary.
    """

    @staticmethod
    def read(config_path: str) -> Dict[str, Any]:
        """
        Read contents of .ini file
        Args:
            config_path:

        Raises:
            ValueError: if config_path is not an .ini file

        Returns:
            Contents of .ini file as a dictionary
        """
        if not config_path.endswith(".ini"):
            raise ValueError(f"IniReader can only read from .ini file! : {config_path}")
        parser = configparser.ConfigParser()
        parser.read(config_path)
        return {k: dict(section) for k, section in dict(parser).items()}


class ConfigLoaderIni(ConfigLoader):
    """
    A class for loading csort configurations from a .ini file

    Methods:
        _set_config_parser: set the parser to be IniReader
        _read_config: read configurations from .ini file
    """

    default_config_file_name = DEFAULT_CONFIG_INI_FILE_NAME

    def _set_config_parser(self) -> IniReader:
        return IniReader()

    def _read_config(self, config_path: str) -> Dict[str, Any]:
        cfg = self._config_parser.read(config_path)

        formatted_csort_cfg = {
            DEFAULT_CSORT_PARAMS_SECTION: cfg[DEFAULT_CSORT_PARAMS_SECTION],
            DEFAULT_CSORT_ORDERING_SECTION: cfg[DEFAULT_CSORT_ORDERING_SECTION],
        }
        self._loaded_config = True
        return formatted_csort_cfg


class TomlReader:
    @staticmethod
    def read(config_path: str) -> Dict[str, Any]:
        """
        Read contents of .toml file
        Args:
            config_path:

        Raises:
            ValueError: if config_path is not an .toml file

        Returns:
            Contents of .toml file as a dictionary
        """
        if not config_path.endswith(".toml"):
            raise ValueError(f"IniReader can only read from .toml file! : {config_path}")
        return toml.load(config_path)


class ConfigLoaderToml(ConfigLoader):
    """
    A class for loading csort configurations from a .toml file

    Methods:
        _set_config_parser: set the parser to be TomlReader
        _read_config: read configurations from .toml file
    """

    default_config_file_name = DEFAULT_CONFIG_TOML_FILE_NAME

    def _set_config_parser(self) -> TomlReader:
        return TomlReader()

    def _read_config(self, config_path: str) -> Dict[str, Any]:
        cfg = self._config_parser.read(config_path)
        # toml can contain non csort related configs
        # toml reads in as csort with order dictionary nested within csort
        csort_cfg = cfg[DEFAULT_CSORT_PARAMS_SECTION]
        if not isinstance(csort_cfg, dict):
            raise TypeError("Expected csort config from toml file to be a dictionary!")
        if DEFAULT_CSORT_ORDERING_SUBSECTION in csort_cfg:
            order = csort_cfg.pop(DEFAULT_CSORT_ORDERING_SUBSECTION)
        else:
            order = {}
        formatted_csort_cfg = {DEFAULT_CSORT_PARAMS_SECTION: csort_cfg, DEFAULT_CSORT_ORDERING_SECTION: order}
        self._loaded_config = True
        return formatted_csort_cfg


CONFIG_LOADERS: Dict[str, Callable] = {".ini": ConfigLoaderIni, ".toml": ConfigLoaderToml}


def get_config_loader(config_path: Optional[str] = None) -> ConfigLoader:
    """
    Instantiate a config loader based on the provided config path.

    If config_path is not None, then match the file suffix to a loader.
    If config_path is None, look for default config files and then create a loader if found.
    Otherwise, a toml loader will be used with defaults

    Args:
        config_path: path to a config file

    Returns:
        Instantiated ConfigLoader

    Raises:
        ValueError: if config path is provided but does not match a loader
    """
    if config_path is not None:
        loader_cls = CONFIG_LOADERS.get(Path(config_path).suffix)
        if loader_cls is None:
            raise ValueError(f"{config_path} config format is not supported! Use .ini or pyproject.toml files!")
        logging.info("Loading csort configurations from %s", config_path)
        return loader_cls(config_path)

    loaders = [cls(config_path) for cls in CONFIG_LOADERS.values()]

    for loader in loaders:
        config_path = loader.get_config_file_path()
        if config_path is not None:
            break
    if config_path is None:
        # just use default configurations so does not matter which loader we use
        logging.info("Loading default csort configurations!")
        return ConfigLoaderToml(config_path=None)
    logging.info("Found %s. Loading csort configurations from %s", config_path, config_path)
    return CONFIG_LOADERS[Path(config_path).suffix](config_path)
