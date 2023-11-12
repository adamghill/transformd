import pytest
from typeguard import TypeCheckError

# Import any fixtures to be used in test functions
from tests.transformer.fixtures import *  # noqa: F403


def test_invalid_type(transformer):
    with pytest.raises(TypeCheckError) as e:
        transformer.transform(spec=1)

    assert 'argument "spec" (int) did not match any element in the union' in e.exconly()


@pytest.mark.skip("For future")
def test_invalid_spec(transformer):
    with pytest.raises(AssertionError) as e:
        transformer.transform(spec="library.blob")

    assert "Unknown key" in e.exconly()


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
