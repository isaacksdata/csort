import os
from unittest.mock import patch

import pytest

from src.config_loader import ConfigLoader
from src.config_loader import ConfigLoaderIni
from src.config_loader import ConfigLoaderToml
from src.config_loader import get_config_loader
from src.config_loader import IniReader
from src.config_loader import TomlReader
from src.configs import DEFAULT_CSORT_ORDER_PARAMS


DEBUG = "tests" in os.getcwd()


@pytest.fixture
def ini_config_path():
    if DEBUG:
        return "./csort.ini"
    return "./tests/unit/csort.ini"


@pytest.fixture
def toml_config_path():
    if DEBUG:
        return "./pyproject_test.toml"
    return "./tests/unit/pyproject_test.toml"


@pytest.fixture
def ini_reader():
    return IniReader()


@pytest.fixture
def toml_reader():
    return TomlReader


@pytest.fixture
def config_no_path():
    return ConfigLoaderIni()


@pytest.fixture
def toml_config_loader():
    return ConfigLoaderToml()


@patch.multiple(ConfigLoader, __abstractmethods__=set())
def test_abstract_config_loader():
    loader = ConfigLoader()
    assert loader._set_config_parser() is None
    assert loader._read_config(config_path="") is None


def test_ini_reader(ini_config_path, ini_reader):
    output = ini_reader.read(ini_config_path)
    assert isinstance(output, dict)
    assert isinstance(output["csort"], dict)


def test_ini_reader_valueerror(ini_reader):
    with pytest.raises(ValueError):
        ini_reader.read("file.txt")


def test_toml_reader(toml_config_path, toml_reader):
    output = toml_reader.read(toml_config_path)
    assert isinstance(output, dict)


def test_toml_reader_valueerror(toml_reader):
    with pytest.raises(ValueError):
        toml_reader.read("file.txt")


def test_config_loader_init(config_no_path):
    assert config_no_path._config_path is None
    assert isinstance(config_no_path._config_parser, IniReader)
    assert not config_no_path._loaded_config


def test_config_loader_init_path():
    config = ConfigLoaderIni(config_path="./test_path/config.ini")
    assert config._config_path == "./test_path/config.ini"


def test_config_loader_locate_config_file(config_no_path):
    output = config_no_path.get_config_file_path()
    assert output.endswith("csort.ini")


def test_config_loader_read_config(config_no_path, ini_config_path):
    cfg = config_no_path._read_config(config_path=ini_config_path)
    assert config_no_path._loaded_config
    assert "csort" in cfg
    assert "csort.order" in cfg


def test_config_loader_load_config(config_no_path):
    cfg = config_no_path._load_config()
    assert config_no_path._loaded_config
    assert "csort" in cfg


def test_config_loader_load_config_with_path(ini_config_path):
    config = ConfigLoaderIni(config_path=ini_config_path)
    cfg = config._load_config()
    assert config._loaded_config
    assert "csort" in cfg


def test_config_loader_config(config_no_path):
    assert not config_no_path._loaded_config
    output = config_no_path.config
    assert isinstance(output, dict)
    assert "csort" in output.keys()
    assert config_no_path._loaded_config
    output2 = config_no_path.config
    assert output2 == output


def test_config_loader_load_defaults(config_no_path):
    cfg = config_no_path._load_defaults()
    assert "csort" in cfg


def test_config_loader_validate_config_file_too_many(config_no_path):
    files = ["csort.ini", "csort2.ini"]
    with pytest.raises(ValueError):
        config_no_path._validate_config_path(files)


def test_config_loader_validate_config_file_no_files(config_no_path):
    output = config_no_path._validate_config_path(config_path=[])
    assert output is None


def test_config_loader_load_config_none(config_no_path, caplog):
    with patch("src.config_loader.ConfigLoader.get_config_file_path", return_value=None):
        cfg = config_no_path._load_config()
    assert "No config file found! Using default behaviours." in caplog.messages
    assert {k: int(v) for k, v in cfg["csort.order"].items()} == DEFAULT_CSORT_ORDER_PARAMS


def test_toml_reader_read(toml_config_path):
    reader = TomlReader()
    output = reader.read(toml_config_path)
    assert isinstance(output, dict)
    assert "csort" in output
    assert "order" in output["csort"]


def test_config_loader_toml_init(toml_config_loader):
    assert isinstance(toml_config_loader._config_parser, TomlReader)


def test_config_loader_toml_read_config(toml_config_loader, toml_config_path):
    output = toml_config_loader._read_config(toml_config_path)
    assert isinstance(output, dict)
    assert "csort" in output
    assert "csort.order" in output
    assert "database" not in output


def test_config_loader_toml_read_config_no_dict(toml_config_loader, toml_config_path):
    with pytest.raises(TypeError):
        with patch("src.config_loader.TomlReader.read", return_value={"csort": 1}):
            toml_config_loader._read_config(toml_config_path)


def test_config_loader_toml_read_config_no_orders(toml_config_loader, toml_config_path):
    with patch("src.config_loader.TomlReader.read", return_value={"csort": {"param": 1}}):
        output = toml_config_loader._read_config(toml_config_path)
    assert isinstance(output, dict)
    assert "csort.order" in output
    assert output["csort.order"] == {}


def test_get_config_loader_valueerror():
    with pytest.raises(ValueError):
        get_config_loader("some-random-file.txt")


def test_get_config_loader_ini():
    output = get_config_loader("csort.ini")
    assert isinstance(output, ConfigLoaderIni)


def test_get_config_loader_toml():
    output = get_config_loader("pyproject.toml")
    assert isinstance(output, ConfigLoaderToml)


def test_get_config_loader_find_ini():
    output = get_config_loader()
    assert isinstance(output, ConfigLoaderIni)


def test_get_config_loader_find_toml():
    with patch("src.config_loader.ConfigLoader.get_config_file_path", return_value="pyproject.toml"):
        output = get_config_loader()
    assert isinstance(output, ConfigLoaderToml)


def test_get_config_loader_defaults():
    with patch("src.config_loader.ConfigLoader.get_config_file_path", return_value=None):
        output = get_config_loader()
    assert isinstance(output, ConfigLoaderToml)
