import pytest

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
