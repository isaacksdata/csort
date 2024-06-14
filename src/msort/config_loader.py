"""
This module contains logic for loading msort configurations from a config file.
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

from .configs import DEFAULT_CONFIG_INI_FILE_NAME
from .configs import DEFAULT_CONFIG_TOML_FILE_NAME
from .configs import DEFAULT_MSORT_GENERAL_PARAMS
from .configs import DEFAULT_MSORT_ORDER_PARAMS
from .configs import DEFAULT_MSORT_ORDERING_SECTION
from .configs import DEFAULT_MSORT_ORDERING_SUBSECTION
from .configs import DEFAULT_MSORT_PARAMS_SECTION
from .configs import Readable


class ConfigLoader(ABC):
    """
    A class for loading msort configurations from a config file

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

    @staticmethod
    def _load_defaults() -> Dict[str, Any]:
        """
        If no file path is provided or found for msort, then default configurations are loaded
        Returns:
            cfg: mapping of default configurations
        """
        cfg = {
            DEFAULT_MSORT_ORDERING_SECTION: DEFAULT_MSORT_ORDER_PARAMS.copy(),
            DEFAULT_MSORT_PARAMS_SECTION: DEFAULT_MSORT_GENERAL_PARAMS.copy(),
        }
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

    @abstractmethod
    def _set_config_parser(self) -> Readable:
        """
        Concrete classes implement this method to instantiate a class which reads from the config file
        Returns:
            an instance which meets the Readable protocol
        """
        pass

    def get_config_file_path(self) -> Optional[str]:
        """
        Wrapper around finding and validating config file paths
        Returns:
            a config file path if a config file is found, else None
        """
        config_files = self._locate_config_file()
        return self._validate_config_path(config_files)

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
            # add in default msort arguments if not supplied
            other_defaults = {
                k: v
                for k, v in self._load_defaults()[DEFAULT_MSORT_PARAMS_SECTION].items()
                if k not in cfg[DEFAULT_MSORT_PARAMS_SECTION]
            }
            cfg[DEFAULT_MSORT_PARAMS_SECTION].update(other_defaults)
        self._config = cfg
        return cfg

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
    A class for loading msort configurations from a .ini file

    Methods:
        _set_config_parser: set the parser to be IniReader
        _read_config: read configurations from .ini file
    """

    default_config_file_name = DEFAULT_CONFIG_INI_FILE_NAME

    def _read_config(self, config_path: str) -> Dict[str, Any]:
        cfg = self._config_parser.read(config_path)

        formatted_msort_cfg = {
            DEFAULT_MSORT_PARAMS_SECTION: cfg[DEFAULT_MSORT_PARAMS_SECTION],
            DEFAULT_MSORT_ORDERING_SECTION: cfg[DEFAULT_MSORT_ORDERING_SECTION],
        }
        self._loaded_config = True
        return formatted_msort_cfg

    def _set_config_parser(self) -> IniReader:
        return IniReader()


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
    A class for loading msort configurations from a .toml file

    Methods:
        _set_config_parser: set the parser to be TomlReader
        _read_config: read configurations from .toml file
    """

    default_config_file_name = DEFAULT_CONFIG_TOML_FILE_NAME

    def _read_config(self, config_path: str) -> Dict[str, Any]:
        cfg = self._config_parser.read(config_path)
        # toml can contain non msort related configs
        # toml reads in as msort with order dictionary nested within msort
        msort_cfg = cfg["tool"][DEFAULT_MSORT_PARAMS_SECTION]
        if not isinstance(msort_cfg, dict):
            raise TypeError("Expected msort config from toml file to be a dictionary!")
        if DEFAULT_MSORT_ORDERING_SUBSECTION in msort_cfg:
            order = msort_cfg.pop(DEFAULT_MSORT_ORDERING_SUBSECTION)
        else:
            order = {}
        formatted_msort_cfg = {DEFAULT_MSORT_PARAMS_SECTION: msort_cfg, DEFAULT_MSORT_ORDERING_SECTION: order}
        self._loaded_config = True
        return formatted_msort_cfg

    def _set_config_parser(self) -> TomlReader:
        return TomlReader()


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
        logging.info("Loading msort configurations from %s", config_path)
        return loader_cls(config_path)

    loaders = [cls(config_path) for cls in CONFIG_LOADERS.values()]

    for loader in loaders:
        config_path = loader.get_config_file_path()
        if config_path is not None:
            break
    if config_path is None:
        # just use default configurations so does not matter which loader we use
        logging.info("Loading default msort configurations!")
        return ConfigLoaderToml(config_path=None)
    logging.info("Found %s. Loading msort configurations from %s", config_path, config_path)
    return CONFIG_LOADERS[Path(config_path).suffix](config_path)
