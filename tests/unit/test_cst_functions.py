import os
from unittest.mock import Mock

import libcst
import pytest

from src.ast_functions import is_class_method
from src.ast_functions import is_getter
from src.ast_functions import is_property
from src.ast_functions import is_setter
from src.ast_functions import is_static_method
from src.cst_functions import extract_class_components
from src.cst_functions import find_classes
from src.cst_functions import is_annotated_class_attribute
from src.cst_functions import is_class_attribute
from src.cst_functions import is_dunder_method
from src.cst_functions import parse_code
from src.cst_functions import update_node
from src.decorators import _get_decorators_cst
from src.decorators import get_decorator_id_cst
from src.utilities import extract_text_from_file
from src.utilities import get_annotated_attribute_name_cst
from src.utilities import get_attribute_name_cst
from src.utilities import get_function_name_cst
from src.utilities import is_class_docstring_cst
from src.utilities import is_ellipsis_cst

DEBUG = "tests" in os.getcwd()


@pytest.fixture
def script_path(request):
    if DEBUG:
        return f"../scripts/{request.param}_input.py"
    return f"./tests/scripts/{request.param}_input.py"


@pytest.fixture
def mock_statement(script_path):
    return extract_text_from_file(script_path)


@pytest.fixture
def mock_cst_module(mock_statement):
    return libcst.parse_module(mock_statement)


def test_update_node_wrong_type():
    cls = {"node": 3, "index": 1}
    with pytest.raises(TypeError):
        update_node(cls, [])


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_cst_extract_classes(mock_cst_module):
    output = find_classes(mock_cst_module)
    assert isinstance(output, dict)
    assert len(output) == 1
    assert "MyClass" in output


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_cst_extract_class_components(mock_cst_module):
    output = extract_class_components(mock_cst_module.body[0])
    assert len(output) == 9
    assert output[0].name.value == "__init__"


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_cst_is_dunder_method(mock_cst_module):
    output = [is_dunder_method(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 9
    assert sum(output) == 2
    assert output[0]
    assert output[5]


def test_cst_is_dunder_method_no_name():
    assert not is_dunder_method(5)


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
    assert len(output) == 9
    assert sum(output) == 1
    assert output[-2]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_static_method(mock_cst_module):
    output = [is_static_method(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 9
    assert sum(output) == 1
    assert output[-3]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_property_method(mock_cst_module):
    output = [is_property(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 9
    assert sum(output) == 1
    assert output[3]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_setter_method(mock_cst_module):
    output = [is_setter(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 9
    assert sum(output) == 1
    assert output[4]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_is_getter_method(mock_cst_module):
    output = [is_getter(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 9
    assert sum(output) == 1
    assert output[-1]


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_get_function_name(mock_cst_module):
    output = get_function_name_cst(mock_cst_module.body[0].body.body[0])
    assert isinstance(output, str)
    assert output == "__init__"


@pytest.mark.parametrize("script_path", ["attributes"], indirect=True)
def test_is_unannotated_attribute(mock_cst_module):
    output = [is_class_attribute(method) for method in mock_cst_module.body[0].body.body]
    assert len(output) == 7
    assert sum(output) == 2
    assert output[1] and output[3]


@pytest.mark.parametrize("script_path", ["attributes"], indirect=True)
def test_is_annotated_attribute(mock_cst_module):
    output = [is_annotated_class_attribute(method) for method in mock_cst_module.body[0].body.body]
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
        parse_code(code=None, file_path=None)


def test_extract_class_components_no_body():
    output = extract_class_components(class_node=5)
    assert isinstance(output, tuple)
    assert len(output) == 0


def test_extract_class_components_no_indentedblock():
    mock_obj = Mock()
    mock_obj.body = "This is the body content"
    with pytest.raises(TypeError):
        extract_class_components(class_node=mock_obj)
