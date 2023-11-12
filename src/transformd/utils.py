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
