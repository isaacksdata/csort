import ast
import os

import csort.ast_functions as AST
import pytest
from csort.decorators import StaticMethodChecker


DEBUG = "tests" in os.getcwd()


@pytest.fixture
def script_path(request):
    if DEBUG:
        return f"../scripts/{request.param}_input.py"
    return f"./tests/scripts/{request.param}_input.py"


@pytest.fixture
def mock_ast_module(script_path):
    return AST.parse_code(file_path=script_path)


@pytest.fixture
def static_method_checker():
    return StaticMethodChecker(parser=AST)


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_update_module_wrong_type(mock_ast_module):
    classes = {"MyClass": {"node": "123", "index": 1}}
    with pytest.raises(TypeError):
        AST.update_module(module=mock_ast_module, classes=classes)


def test_update_node_attribute_error():
    cls = {"node": "123", "index": 1}
    components = [1, 2, 3]
    with pytest.raises(AttributeError):
        AST.update_node(cls=cls, components=components)


def test_parse_code_str():
    output = AST.parse_code(code="x = 1 + 2")
    assert isinstance(output, ast.Module)


@pytest.mark.parametrize("script_path", ["basic"], indirect=True)
def test_parse_code_file(script_path):
    output = AST.parse_code(file_path=script_path)
    assert isinstance(output, ast.Module)


def test_parse_code_error():
    with pytest.raises(ValueError):
        AST.parse_code(file_path=None, code=None)


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_could_be_static_true(mock_ast_module, static_method_checker):
    output = static_method_checker._check_for_static_ast(mock_ast_module.body[1].body[6])
    assert output


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_could_be_static_false(mock_ast_module, static_method_checker):
    output = static_method_checker._check_for_static_ast(mock_ast_module.body[1].body[7])
    assert not output


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_could_be_static_false_multi(mock_ast_module, static_method_checker):
    output = static_method_checker._check_for_static_ast(mock_ast_module.body[1].body[8])
    assert not output


@pytest.mark.parametrize("script_path", ["auto_static"], indirect=True)
def test_make_static_ast(mock_ast_module, static_method_checker):
    output = static_method_checker._make_static_ast(mock_ast_module.body[1].body[6])
    assert isinstance(output, ast.FunctionDef)
    assert len(output.decorator_list) == 1
    assert len(output.args.args) == 0
