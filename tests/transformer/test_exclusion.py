import pytest

# Import any fixtures to be used in test functions
from tests.transformer.fixtures import *
from transformd.exceptions import InvalidSpecError


def test_invalid(transformer):
    expected = "'missing' is invalid"

    with pytest.raises(InvalidSpecError) as e:
        transformer.transform(spec="-missing")

    assert expected in e.exconly()


def test_invalid_nested(transformer):
    expected = "'missing' is invalid"

    with pytest.raises(InvalidSpecError) as e:
        transformer.transform(spec="-missing.name")

    assert expected in e.exconly()


def test_invalid_nested_2(transformer):
    expected = "'missing' is invalid"

    with pytest.raises(InvalidSpecError) as e:
        transformer.transform(spec="-library.missing")

    assert expected in e.exconly()


def test_whole(transformer):
    expected = {}

    actual = transformer.transform(spec="-library")

    assert expected == actual


def test_nested(transformer):
    expected = {
        "library": {
            "name": "Main St Library",
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

    actual = transformer.transform(spec="-library.location")

    assert expected == actual


def test_multiple(transformer):
    expected = {"library": {"name": "Main St Library"}}

    spec = (
        "-library.location",
        "-library.books",
    )
    actual = transformer.transform(spec=spec)

    assert expected == actual


def test_list(transformer):
    expected = {
        "library": {
            "books": [
                {
                    "title": "Slaughterhouse-Five",
                    "author": {"first_name": "Kurt", "last_name": "Vonnegut"},
                },
            ],
        }
    }

    spec = (
        "-library.location",
        "-library.name",
        "-library.books.0",
    )
    actual = transformer.transform(spec=spec)

    assert expected == actual


def test_list_with_nest(transformer):
    expected = {
        "library": {
            "books": [
                {
                    "title": "Slaughterhouse-Five",
                },
            ],
        }
    }

    spec = (
        "-library.location",
        "-library.name",
        "-library.books.0",
        "-library.books.0.author",
    )
    actual = transformer.transform(spec=spec)

    assert expected == actual
