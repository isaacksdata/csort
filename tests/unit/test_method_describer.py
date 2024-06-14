import ast
import configparser
from copy import deepcopy
from typing import Callable
from unittest.mock import patch

import pytest
from csort.generic_functions import is_class_method
from csort.method_describers import ASTMethodDescriber
from csort.method_describers import CSTMethodDescriber
from csort.method_describers import get_method_describer
from csort.method_describers import MethodDescriber


@pytest.fixture
def mock_config():
    config = configparser.ConfigParser()
    config["csort.order"] = {}
    config["csort.order"]["dunder_method"] = "3"
    config["csort.order"]["csort_group"] = "4"
    config["csort.order"]["class_method"] = "5"
    config["csort.order"]["static_method"] = "6"
    config["csort.order"]["property"] = "7"
    config["csort.order"]["decorated_method"] = "10"
    config["csort.order"]["instance_method"] = "12"
    config["csort.order"]["private_method"] = "13"
    return config


@pytest.fixture
def func_source_code():
    return "def func() -> int:\n    return 1"


@pytest.fixture
def static_func(func_source_code):
    return "@staticmethod\n" + func_source_code


@pytest.fixture
def class_func(func_source_code):
    return "@classmethod\n" + func_source_code


@pytest.fixture
def cached_func(func_source_code):
    return "@lru_cache\n" + func_source_code


@pytest.fixture
def csort_group_func(func_source_code):
    return "@csort_group(group='test')\n" + func_source_code


@pytest.fixture
def private_func(func_source_code):
    return func_source_code.replace("func", "_func")


@patch.multiple(MethodDescriber, __abstractmethods__=set())
def test_abstract_config_loader():
    describer = MethodDescriber()
    assert describer._non_method_defaults() is None
    assert describer._validate_node(node="") is None
    assert describer._setup_config_to_func_map is None


def test_ast_method_describer_init(mock_config):
    describer = ASTMethodDescriber(config=mock_config)
    assert isinstance(describer._config, configparser.ConfigParser)
    for key, func in describer._config_to_func_map.items():
        assert isinstance(key, str)
        assert isinstance(func, Callable)
    for func, value in describer._method_checking_map.items():
        assert isinstance(func, Callable)
        assert isinstance(value, int)
    method_levels = list(describer._method_checking_map.values())
    assert all(m in method_levels for m in list(map(int, list(mock_config["csort.order"].values()))))


def test_ast_method_describer__setup_func_to_level_map_valueerror(mock_config):
    mock_config["csort.order"]["class_method"] = "1"
    with pytest.raises(ValueError):
        ASTMethodDescriber(config=mock_config)


def test_ast_method_describer__setup_func_to_level_map_override(mock_config, caplog):
    mock_config["csort.order"]["class_method"] = "1"
    describer = ASTMethodDescriber(config=mock_config, override_level_check=True)
    msg = "The sorting level for ['class_method'] is 1 which is higher than max default 2. Exception overridden by --force option."
    assert msg in caplog.messages
    assert describer._method_checking_map[is_class_method] == 1


def test_ast_method_describer_describe_method(
    mock_config, func_source_code, static_func, class_func, cached_func, private_func, csort_group_func
):
    describer = ASTMethodDescriber(config=deepcopy(mock_config))
    for func_code, expected_value in zip(
        [func_source_code, static_func, class_func, cached_func, private_func, csort_group_func],
        [
            mock_config["csort.order"]["instance_method"],
            mock_config["csort.order"]["static_method"],
            mock_config["csort.order"]["class_method"],
            mock_config["csort.order"]["decorated_method"],
            mock_config["csort.order"]["private_method"],
            mock_config["csort.order"]["csort_group"],
        ],
    ):
        node = ast.parse(func_code).body[0]
        output = describer.get_method_type(node)
        assert output == int(expected_value)


def test_ast_method_describer_get_method_type_typeerror(mock_config):
    describer = ASTMethodDescriber(config=mock_config)
    with pytest.raises(TypeError):
        describer.get_method_type(method=1)


def test_get_method_describer(mock_config):
    assert isinstance(get_method_describer("ast", config=mock_config), ASTMethodDescriber)
    assert isinstance(get_method_describer("cst", config=mock_config), CSTMethodDescriber)
    with pytest.raises(KeyError):
        get_method_describer("null")
