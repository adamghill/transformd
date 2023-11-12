import pytest
from typeguard import TypeCheckError

# Import any fixtures to be used in test functions
from tests.transformer.fixtures import *  # noqa: F403
from transformd import InvalidSpecError


def test_invalid_type(transformer):
    with pytest.raises(TypeCheckError) as e:
        transformer.transform(spec=1)

    assert 'argument "spec" (int) did not match any element in the union' in e.exconly()


def test_invalid_spec(transformer):
    with pytest.raises(InvalidSpecError) as e:
        transformer.transform(spec="library.missing")

    assert "'missing' is invalid" in e.exconly()


def test_invalid_spec_exception_has_data(transformer):
    with pytest.raises(InvalidSpecError) as e:
        transformer.transform(spec="library.missing")

    expected_key = "missing"
    assert expected_key == e.value.key

    expected_data = transformer.data["library"]
    assert expected_data == e.value.data


def test_invalid_spec_ignore_invalid(transformer):
    expected = {"library": {}}
    actual = transformer.transform(spec="library.missing", ignore_invalid=True)

    assert expected == actual


def test_whole_object_with_string_spec(transformer):
    expected = transformer.data.copy()
    actual = transformer.transform(spec="library")

    assert expected == actual


def test_whole_object_with_tuple_spec(transformer):
    expected = transformer.data.copy()
    actual = transformer.transform(spec=("library",))

    assert expected == actual


def test_whole_object_with_list_spec(transformer):
    expected = transformer.data.copy()
    actual = transformer.transform(
        spec=[
            "library",
        ]
    )

    assert expected == actual
