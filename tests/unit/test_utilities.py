import pytest
from csort.utilities import check_and_get_attribute


def test_check_attribute_success():
    assert check_and_get_attribute("a string", "lower") is not None


def test_check_attribute_fail():
    assert check_and_get_attribute(3, "lower") is None


def test_check_attribute_exception():
    with pytest.raises(AttributeError):
        check_and_get_attribute(3, "lower", raise_exception=True)
