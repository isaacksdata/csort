import ast
from unittest.mock import Mock

import libcst
import pytest
from msort.decorators import decorator_attribute_id_cst
from msort.decorators import decorator_call_id
from msort.decorators import decorator_call_id_cst
from msort.decorators import decorator_name_id_cst
from msort.decorators import get_decorator_id
from msort.decorators import get_decorator_id_cst
from msort.decorators import get_msort_group_name_ast
from msort.decorators import get_msort_group_name_cst
from msort.decorators import has_decorator


def test_decorator_call_id_attribute_error():
    mock_decorator = Mock()
    mock_decorator.func = "mocked function"
    with pytest.raises(AttributeError):
        decorator_call_id(mock_decorator)


def test_decorator_name_id_attribute_error():
    mock_decorator = Mock()
    mock_decorator.decorator = "mocked decorator"
    with pytest.raises(AttributeError):
        decorator_name_id_cst(mock_decorator)


def test_decorator_attribute_id_attribute_error():
    mock_decorator = Mock()
    mock_decorator.decorator = "mocked decorator"
    with pytest.raises(AttributeError):
        decorator_attribute_id_cst(mock_decorator)


def test_decorator_call_id_cst_attribute_error():
    with pytest.raises(AttributeError):
        decorator_call_id_cst(3)


def test_get_decorator_id():
    with pytest.raises(TypeError):
        get_decorator_id(1)


def test_get_decorator_id_cst():
    mock_decorator = Mock()
    mock_decorator.decorator = "mocked decorator"
    with pytest.raises(TypeError):
        get_decorator_id_cst(mock_decorator)


def test_has_decorator_false():
    mock_decorator = Mock()
    mock_decorator.decorator = "mocked decorator"
    assert not has_decorator(mock_decorator, "mock")


def test_get_msort_group_name_ast():
    code = '@msort_group(group="test")\ndef func():\n\tpass\n'
    node = ast.parse(code)
    output = get_msort_group_name_ast(node.body[0])
    assert output == "test"


def test_get_msort_group_name_ast_no_decorator_attr():
    code = '@msort_group(group="test")\ndef func():\n\tpass\n'
    node = ast.parse(code)
    output = get_msort_group_name_ast(node)
    assert output is None


def test_get_msort_group_name_ast_no_decorators():
    code = "def func():\n\tpass\n"
    node = ast.parse(code)
    output = get_msort_group_name_ast(node.body[0])
    assert output is None


def test_get_msort_group_name_ast_no_call_decorators():
    code = "@msort_group\ndef func():\n\tpass\n"
    node = ast.parse(code)
    output = get_msort_group_name_ast(node.body[0])
    assert output is None


def test_get_msort_group_name_ast_no_keyword_value():
    code = '@msort_group(group="")\ndef func():\n\tpass\n'
    node = ast.parse(code)
    # override the constant so there is no value attribute
    node.body[0].decorator_list[0].keywords[0].value = 1
    output = get_msort_group_name_ast(node.body[0])
    assert output is None


def test_get_msort_group_name_ast_no_arg_value():
    code = '@msort_group("")\ndef func():\n\tpass\n'
    node = ast.parse(code)
    # override the constant so there is no value attribute
    node.body[0].decorator_list[0].args[0] = 1
    output = get_msort_group_name_ast(node.body[0])
    assert output is None


def test_get_msort_group_name_cst():
    code = "@msort_group(group=test)\ndef func():\n\tpass\n"
    node = libcst.parse_module(code)
    output = get_msort_group_name_cst(node.body[0])
    assert output == "test"


def test_get_msort_group_name_cst_no_decorators():
    code = "def func():\n\tpass\n"
    node = libcst.parse_module(code)
    output = get_msort_group_name_cst(node.body[0])
    assert output is None


def test_get_msort_group_name_cst_no_args():
    code = "@msort_group\ndef func():\n\tpass\n"
    node = libcst.parse_module(code)
    with pytest.raises(AttributeError):
        get_msort_group_name_cst(node.body[0])
