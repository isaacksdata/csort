import logging
import os
from unittest.mock import Mock

import libcst
import msort.cst_functions as CST
import pytest
from msort.ast_functions import is_class_method
from msort.ast_functions import is_getter
from msort.ast_functions import is_property
from msort.ast_functions import is_setter
from msort.ast_functions import is_static_method
from msort.decorators import _get_decorators_cst
from msort.decorators import get_decorator_id_cst
from msort.decorators import StaticMethodChecker
from msort.utilities import extract_text_from_file
from msort.utilities import get_annotated_attribute_name_cst
from msort.utilities import get_attribute_name_cst
from msort.utilities import get_function_name_cst
from msort.utilities import is_class_docstring_cst
from msort.utilities import is_ellipsis_cst

if os.getcwd().endswith("unit"):
    os.chdir("../..")

DEBUG = "tests" in os.getcwd()


@pytest.fixture
def script_path(request):
    # if DEBUG:
    # return f"../scripts/{request.param}_input.py"
    return f"./tests/scripts/{request.param}_input.py"


@pytest.fixture
def mock_statement(script_path):
    return extract_text_from_file(script_path)


@pytest.fixture
def mock_cst_module(mock_statement):
    return libcst.parse_module(mock_statement)


@pytest.fixture
def static_method_checker():
    return StaticMethodChecker(parser=CST)


def test_update_node_wrong_type():
    cls = {"node": 3, "index": 1}
    with pytest.raises(TypeError):
        CST.update_node(cls, [])


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_cst_extract_classes(mock_cst_module):
    output = CST.find_classes(mock_cst_module)
    assert isinstance(output, dict)
    assert len(output) == 1
    assert "MyClass" in output


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_cst_extract_class_components(mock_cst_module):
    output = CST.extract_class_components(mock_cst_module.body[0])
    assert len(output) == 10
    assert output[0].name.value == "__init__"


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_cst_is_dunder_method(mock_cst_module):
    output = [CST.is_dunder_method(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 10
    assert sum(output) == 2
    assert output[0]
    assert output[5]


def test_cst_is_dunder_method_no_name():
    assert not CST.is_dunder_method(5)


@pytest.mark.parametrize("script_path", ["multi_decorators"], indirect=True)
def test_get_decorator_id_cst(mock_cst_module):
    output = get_decorator_id_cst(mock_cst_module.body[3].body.body[7].decorators[0])
    assert output == "lru_cache"


@pytest.mark.parametrize("script_path", ["multi_decorators"], indirect=True)
def test_get_decorators_cst(mock_cst_module):
    output = _get_decorators_cst(mock_cst_module.body[3].body.body[7])
    assert output == ["lru_cache", "staticmethod"]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_class_method(mock_cst_module):
    output = [is_class_method(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 10
    assert sum(output) == 1
    assert output[-3]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_static_method(mock_cst_module):
    output = [is_static_method(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 10
    assert sum(output) == 1
    assert output[-4]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_property_method(mock_cst_module):
    output = [is_property(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 10
    assert sum(output) == 1
    assert output[3]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_setter_method(mock_cst_module):
    output = [is_setter(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 10
    assert sum(output) == 1
    assert output[4]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_getter_method(mock_cst_module):
    output = [is_getter(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 10
    assert sum(output) == 1
    assert output[-1]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_get_function_name(mock_cst_module):
    output = get_function_name_cst(mock_cst_module.body[0].body.body[0])
    assert isinstance(output, str)
    assert output == "__init__"


@pytest.mark.parametrize("script_path", ["attributes"], indirect=True)
def test_is_unannotated_attribute(mock_cst_module):
    output = [CST.is_class_attribute(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 7
    assert sum(output) == 2
    assert output[1] and output[3]


@pytest.mark.parametrize("script_path", ["attributes"], indirect=True)
def test_is_annotated_attribute(mock_cst_module):
    output = [CST.is_annotated_class_attribute(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 7
    assert sum(output) == 2
    assert output[0] and output[5]


@pytest.mark.parametrize("script_path", ["attributes"], indirect=True)
def test_get_annotated_attribute_name(mock_cst_module):
    output = get_annotated_attribute_name_cst(mock_cst_module.body[0].body.body[0])
    assert isinstance(output, str)
    assert output == "name"


@pytest.mark.parametrize("script_path", ["attributes"], indirect=True)
def test_get_attribute_name(mock_cst_module):
    output = get_attribute_name_cst(mock_cst_module.body[0].body.body[1])
    assert isinstance(output, str)
    assert output == "untyped_attribute"


@pytest.mark.parametrize("script_path", ["docstrings_comments"], indirect=True)
def test_is_class_docstring(mock_cst_module):
    output = [is_class_docstring_cst(method) for method in mock_cst_module.body[1].body.body]
    assert len(output) == 11
    assert sum(output) == 1
    assert output[0]


@pytest.mark.parametrize("script_path", ["empty"], indirect=True)
def test_is_ellipsis(mock_cst_module):
    output = [is_ellipsis_cst(method) for method in mock_cst_module.body[1].body.body]
    assert len(output) == 3
    assert sum(output) == 1
    assert output[0]


def test_parse_code():
    with pytest.raises(ValueError):
        CST.parse_code(code=None, file_path=None)


def test_extract_class_components_no_body():
    output = CST.extract_class_components(class_node=5)
    assert isinstance(output, tuple)
    assert len(output) == 0


def test_extract_class_components_no_indentedblock():
    mock_obj = Mock()
    mock_obj.body = "This is the body content"
    with pytest.raises(TypeError):
        CST.extract_class_components(class_node=mock_obj)


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_could_be_static_true(mock_cst_module, static_method_checker):
    output = static_method_checker._check_for_static_cst(mock_cst_module.body[1].body.body[6])
    assert output


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_could_be_static_false(mock_cst_module, static_method_checker):
    output = static_method_checker._check_for_static_cst(mock_cst_module.body[1].body.body[7])
    assert not output


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_could_be_static_false_multi(mock_cst_module, static_method_checker):
    output = static_method_checker._check_for_static_cst(mock_cst_module.body[1].body.body[8])
    assert not output


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_could_be_static_already_static(mock_cst_module, static_method_checker):
    output = static_method_checker._check_for_static(mock_cst_module.body[1].body.body[9])
    assert not output


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_could_be_static_abstract(mock_cst_module, static_method_checker):
    output = static_method_checker._check_for_static(mock_cst_module.body[1].body.body[12])
    assert not output


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_make_static_cst(mock_cst_module, static_method_checker):
    output = static_method_checker._make_static_cst(mock_cst_module.body[1].body.body[6])
    assert isinstance(output, libcst.FunctionDef)
    assert len(output.decorators) == 1
    assert len(output.params.params) == 0
