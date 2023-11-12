import pytest
from typeguard import TypeCheckError

from transformd import Transformer


@pytest.fixture
def transformer():
    data = {
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

    return Transformer(data)


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


def test_nested(transformer):
    expected = {
        "library": {
            "location": {
                "street": "123 Main St",
                "city": "New York City",
                "state": "NY",
            },
        }
    }

    actual = transformer.transform(spec=("library.location",))

    assert expected == actual


def test_nested_multiple(transformer):
    expected = {"library": {"location": {"street": "123 Main St"}}}

    actual = transformer.transform(spec=("library.location.street",))

    assert expected == actual


def test_multiple_nested(transformer):
    expected = {
        "library": {
            "name": "Main St Library",
            "location": {
                "state": "NY",
            },
        }
    }

    actual = transformer.transform(
        spec=(
            "library.name",
            "library.location.state",
        )
    )

    assert actual == expected


def test_multiple_overridden(transformer):
    expected = {
        "library": {
            "location": {
                "street": "123 Main St",
                "city": "New York City",
                "state": "NY",
            }
        }
    }

    actual = transformer.transform(
        spec=(
            "library.location",
            "library.location.street",
        )
    )

    assert actual == expected


def test_multiple_overridden_2(transformer):
    expected = {
        "library": {
            "location": {
                "street": "123 Main St",
                "city": "New York City",
                "state": "NY",
            }
        }
    }

    actual = transformer.transform(
        spec=(
            "library.location.street",
            "library.location",
        )
    )

    assert actual == expected


def test_list(transformer):
    expected = {
        "library": {
            "books": [
                {
                    "author": {"first_name": "John", "last_name": "Steinbeck"},
                },
                {
                    "author": {"first_name": "Kurt", "last_name": "Vonnegut"},
                },
            ],
        }
    }

    actual = transformer.transform(
        spec=(
            "library.books.0.author",
            "library.books.1.author",
        )
    )

    assert expected == actual


def test_list_with_nested(transformer):
    expected = {
        "library": {
            "books": [
                {
                    "author": {"last_name": "Steinbeck"},
                },
                {
                    "author": {"first_name": "Kurt", "last_name": "Vonnegut"},
                },
            ],
        }
    }

    actual = transformer.transform(
        spec=(
            "library.books.0.author.last_name",
            "library.books.1.author",
        )
    )

    assert expected == actual


def test_entire_list(transformer):
    expected = {
        "library": {
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

    actual = transformer.transform(spec=("library.books",))

    assert expected == actual


def test_list_with_index(transformer):
    expected = {
        "library": {
            "books": [
                {
                    "title": "The Grapes of Wrath",
                    "author": {"first_name": "John", "last_name": "Steinbeck"},
                },
                {
                    "author": {"first_name": "Kurt", "last_name": "Vonnegut"},
                },
            ],
        }
    }

    actual = transformer.transform(
        spec=(
            "library.books.0",
            "library.books.1.author",
        )
    )

    assert expected == actual
