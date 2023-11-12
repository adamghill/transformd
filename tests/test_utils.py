from transformd.utils import is_int


def test_is_int_string():
    actual = is_int("asdf")

    assert actual is False


def test_is_int_integer():
    actual = is_int(1)

    assert actual is True


def test_is_int_string_integer():
    actual = is_int("1")

    assert actual is True
