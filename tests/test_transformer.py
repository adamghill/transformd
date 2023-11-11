import pytest

from transformd import DictionaryTransformer


@pytest.fixture
def data():
    return {
        "library": {
            "name": "Main St Library",
            "location": {
                "street": "123 Main St",
                "city": "New York City",
                "state": "NY",
            },
            "books": [
                {
                    "title": "The Grapes of Wrath",
                    "author": {"first_name": "John", "last_name": "Steinbeck"},
                },
                {
                    "title": "Slaughterhouse-Five",
                    "author": {"first_name": "Kurt", "last_name": "Vonnegut"},
                },
            ],
        }
    }


def test_whole_object(data):
    expected = data.copy()
    actual = DictionaryTransformer(data).transform(spec=("library",))

    assert expected == actual


def test_whole_object_with_string_spec(data):
    expected = data.copy()
    actual = DictionaryTransformer(data).transform(spec="library")

    assert expected == actual


def test_nested(data):
    expected = {"library": {"location": {"street": "123 Main St"}}}

    actual = DictionaryTransformer(data).transform(spec=("library.location.street",))

    assert expected == actual
