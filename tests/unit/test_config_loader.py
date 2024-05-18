import configparser
import os
from unittest.mock import patch

import pytest

from src.config_loader import ConfigLoader
from src.configs import DEFAULT_CSORT_ORDER_PARAMS


DEBUG = "tests" in os.getcwd()


@pytest.fixture
def config_path():
    if DEBUG:
        return "./csort.ini"
    return "./tests/unit/csort.ini"


@pytest.fixture
def config_no_path():
    return ConfigLoader()


def test_config_loader_init(config_no_path):
    assert config_no_path._config_path is None
    assert isinstance(config_no_path._config_parser, configparser.ConfigParser)
    assert not config_no_path._loaded_config


def test_config_loader_init_path():
    config = ConfigLoader(config_path="./test_path/config.ini")
    assert config._config_path == "./test_path/config.ini"


def test_config_loader_locate_config_file(config_no_path):
    output = config_no_path._get_config_file_path()
    assert output.endswith("csort.ini")


def test_config_loader_read_config(config_no_path, config_path):
    config_no_path._read_config(config_path=config_path)
    assert config_no_path._loaded_config
    assert "csort" in config_no_path.config.keys()


def test_config_loader_load_config(config_no_path):
    config_no_path._load_config()
    assert config_no_path._loaded_config
    assert "csort" in config_no_path.config.keys()


def test_config_loader_load_config_with_path(config_path):
    config = ConfigLoader(config_path=config_path)
    config._load_config()
    assert config._loaded_config
    assert "csort" in config.config.keys()


def test_config_loader_config(config_no_path):
    assert not config_no_path._loaded_config
    output = config_no_path.config
    assert isinstance(output, configparser.ConfigParser)
    assert "csort" in output.keys()


def test_config_loader_load_defaults(config_no_path):
    config_no_path._load_defaults()
    assert "csort" in config_no_path._config_parser.keys()


def test_config_loader_validate_config_file_too_many(config_no_path):
    files = ["csort.ini", "csort2.ini"]
    with pytest.raises(ValueError):
        config_no_path._validate_config_path(files)


def test_config_loader_validate_config_file_no_files(config_no_path):
    output = config_no_path._validate_config_path(config_path=[])
    assert output is None


def test_config_loader_load_config_none(config_no_path, caplog):
    with patch("src.config_loader.ConfigLoader._get_config_file_path", return_value=None):
        config_no_path._load_config()
    assert "No config file found! Using default behaviours." in caplog.messages
    assert {k: int(v) for k, v in config_no_path.config["csort.order"].items()} == DEFAULT_CSORT_ORDER_PARAMS
