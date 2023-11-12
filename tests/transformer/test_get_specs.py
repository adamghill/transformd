import pytest
from typeguard import TypeCheckError

# Import any fixtures to be used in test functions
from tests.transformer.fixtures import *  # noqa: F403


def test_string(transformer):
    expected = [
        "test",
    ]
    actual = transformer._get_specs("test")

    assert expected == actual


def test_list(transformer):
    expected = [
        "test",
    ]
    actual = transformer._get_specs(
        [
            "test",
        ]
    )

    assert expected == actual


def test_tuple(transformer):
    expected = ("test",)
    actual = transformer._get_specs(("test",))

    assert expected == actual


def test_invalid_type(transformer):
    with pytest.raises(TypeCheckError) as e:
        transformer._get_specs(1)

    assert 'argument "spec" (int) did not match any element in the union' in e.exconly()
