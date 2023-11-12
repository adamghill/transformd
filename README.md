# transformd

Transform a `dictionary` to another `dictionary`, but keep the same shape based on a `spec`.

## What is a spec?

It is a string (or sequence of strings) that specifies what "parts" of the dictionary should be included in a new `dictionary` that is returned from the `transform` function. A `spec` uses dot-notation to traverse into the `dictionary`. It can also use indexes if the object is a list.

## Examples

```python
from transformd import Transformer

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

assert Transformer(data).transform(spec="library.name") == {
    "library": {
        "name": "Main St Library"
    }
}

assert Transformer(data).transform(spec=("library.name", "library.location.state")) == {
    "library": {
        "name": "Main St Library",
        "location": {
            "state": "NY"
        },
    }
}

assert Transformer(data).transform(spec=("library.books.0.title", "library.books.1")) == {
    "library": {
        "books": [
            {
                "title": "The Grapes of Wrath",
            },
            {
                "title": "Slaughterhouse-Five",
                "author": {"first_name": "Kurt", "last_name": "Vonnegut"},
            },
        ],
    }
}
```

## Why?

I needed this functionality for [`Unicorn`](https://www.django-unicorn.com), but could not find a suitable library. After writing the code, I thought maybe it would be useful for someone else. 🤷

## Run tests

`rye sync && rye run test`

## Inspiration

- Django Templates for the dot-notation inspiration
- A lot of existing JSON-related tools, but especially [`glom`](https://glom.readthedocs.io/), [`jello`](https://github.com/kellyjonbrazil/jello), [`jq`](https://jqlang.github.io/jq/), and [`gron`](https://github.com/TomNomNom/gron); all of which did not quite do what I wanted, but were useful on the journey
