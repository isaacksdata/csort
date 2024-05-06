import pytest

from src.csort_decorator import csort_group


def my_func():
    return 1


class MyClass:
    def my_func(self):
        return 1

    @classmethod
    def my_class_func(cls):
        return 1

    @staticmethod
    def my_static_func():
        return 1


def test_csort_group_failure():
    with pytest.raises(TypeError):
        csort_group(group="test")(1)


def test_csort_group_log_warning(caplog):
    csort_group(group="test")(my_func)
    assert (
        "csort_group decorator applied to a function which is not implemented by a class : my_func" in caplog.messages
    )


def test_csort_group_instance_method(caplog):
    caplog.set_level("DEBUG")
    my_class = MyClass()
    output = csort_group(group="test")(my_class.my_func)()
    assert output == 1
    assert "Calling MyClass.my_func with csort_group : group = test" in caplog.messages


def test_csort_group_class_method(caplog):
    caplog.set_level("DEBUG")
    my_class = MyClass()
    output = csort_group(group="test")(my_class.my_class_func)()
    assert output == 1
    assert "Calling MyClass.my_class_func with csort_group : group = test" in caplog.messages


def test_csort_group_static_method(caplog):
    caplog.set_level("DEBUG")
    my_class = MyClass()
    output = csort_group(group="test")(my_class.my_static_func)()
    assert output == 1
    assert "Calling MyClass.my_static_func with csort_group : group = test" in caplog.messages
