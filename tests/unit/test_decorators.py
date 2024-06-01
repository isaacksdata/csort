from unittest.mock import Mock

import pytest
from csort.decorators import decorator_attribute_id_cst
from csort.decorators import decorator_call_id
from csort.decorators import decorator_call_id_cst
from csort.decorators import decorator_name_id_cst
from csort.decorators import get_decorator_id
from csort.decorators import get_decorator_id_cst
from csort.decorators import has_decorator


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
