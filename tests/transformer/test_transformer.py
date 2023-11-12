# Import any fixtures to be used in test functions
from tests.transformer.fixtures import *  # noqa: F403


def test_both_inclusion_and_exclusion(transformer):
    expected = {
        "library": {
            "books": [
                {
                    "title": "The Grapes of Wrath",
                    "author": {"first_name": "John", "last_name": "Steinbeck"},
                },
            ],
        }
    }

    spec = (
        "library.name",
        "library.books.0",
        "-library.name",
    )
    actual = transformer.transform(spec=spec)

    assert expected == actual
