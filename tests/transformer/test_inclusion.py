# Import any fixtures to be used in test functions
from tests.transformer.fixtures import *  # noqa: F403


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

    spec = ("library.location",)
    actual = transformer.transform(spec=spec)

    assert expected == actual


def test_nested_multiple(transformer):
    expected = {"library": {"location": {"street": "123 Main St"}}}

    spec = ("library.location.street",)
    actual = transformer.transform(spec=spec)

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

    spec = (
        "library.name",
        "library.location.state",
    )
    actual = transformer.transform(spec=spec)

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

    spec = (
        "library.location",
        "library.location.street",
    )
    actual = transformer.transform(spec=spec)

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

    spec = (
        "library.location.street",
        "library.location",
    )
    actual = transformer.transform(spec=spec)

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

    spec = (
        "library.books.0.author",
        "library.books.1.author",
    )
    actual = transformer.transform(spec=spec)

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

    spec = (
        "library.books.0.author.last_name",
        "library.books.1.author",
    )
    actual = transformer.transform(spec=spec)

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

    spec = ("library.books",)
    actual = transformer.transform(spec=spec)

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

    spec = (
        "library.books.0",
        "library.books.1.author",
    )
    actual = transformer.transform(spec=spec)

    assert expected == actual
