import collections


def is_non_string_sequence(obj):
    """
    Checks whether the object is a sequence (i.e. `list`, `tuple`, `set`), but _not_ `str` or `bytes` type.
    Helpful when you expect to loop over `obj`, but explicitly don't want to allow `str`.
    """

    if (isinstance(obj, (collections.abc.Sequence, collections.abc.Set))) and not isinstance(
        obj, (str, bytes, bytearray)
    ):
        return True

    return False


def is_int(s: str) -> bool:
    """
    Checks whether a string is actually an integer.
    """

    try:
        int(s)
    except ValueError:
        return False
    else:
        return True
