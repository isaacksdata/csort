import ast
import configparser
from copy import deepcopy
from typing import Callable

import pytest

from src.functions import ASTMethodDescriber


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
    config["csort.order"]["instance_method"] = "11"
    config["csort.order"]["private_method"] = "12"
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
