import configparser
import os

import pytest

from src.config_loader import ConfigLoader


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
    output = config_no_path._locate_config_file()
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
