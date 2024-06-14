import pytest
from msort.msort_decorator import msort_group


def my_func():
    return 1


class MyClass:
    @classmethod
    def my_class_func(cls):
        return 1

    @staticmethod
    def my_static_func():
        return 1

    def my_func(self):
        return 1


def test_msort_group_failure():
    with pytest.raises(TypeError):
        msort_group(group="test")(1)


def test_msort_group_log_warning(caplog):
    msort_group(group="test")(my_func)
    assert (
        "msort_group decorator applied to a function which is not implemented by a class : my_func" in caplog.messages
    )


def test_msort_group_instance_method(caplog):
    caplog.set_level("DEBUG")
    my_class = MyClass()
    output = msort_group(group="test")(my_class.my_func)()
    assert output == 1
    assert "Calling MyClass.my_func with msort_group : group = test" in caplog.messages


def test_msort_group_class_method(caplog):
    caplog.set_level("DEBUG")
    my_class = MyClass()
    output = msort_group(group="test")(my_class.my_class_func)()
    assert output == 1
    assert "Calling MyClass.my_class_func with msort_group : group = test" in caplog.messages


def test_msort_group_static_method(caplog):
    caplog.set_level("DEBUG")
    my_class = MyClass()
    output = msort_group(group="test")(my_class.my_static_func)()
    assert output == 1
    assert "Calling MyClass.my_static_func with msort_group : group = test" in caplog.messages
