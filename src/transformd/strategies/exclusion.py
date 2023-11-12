from transformd.exceptions import InvalidSpecError
from transformd.utils import is_int

NESTED_PIECES_COUNT = 2


def process(data: dict, spec: str, ignore_invalid: bool = False) -> None:
    """Handle exclusion specs, i.e. specs that specify which parts of the original dictionary to exclude
    from a new dictionary. This will be any spec that starts with a dash.

    Args:
        data: The original data. Gets modified in place.
        spec: Specifies the data to return.
        ignore_invalid: Whether to ignore an invalid spec or not. Raises `InvalidSpecError`
            if `False` and the spec is invalid. Defaults to `False`.
    """

    # Break the spec into a list of pieces based on dot notation
    pieces = spec.split(".")

    if len(pieces) <= 1:
        piece = pieces[0]

        if piece not in data and not ignore_invalid:
            raise InvalidSpecError(key=piece, data=data)

        del data[piece]
    elif len(pieces) == NESTED_PIECES_COUNT:
        (first_piece, second_piece) = pieces

        if first_piece not in data:
            raise InvalidSpecError(key=first_piece, data=data)

        if data[first_piece] is not None:
            if second_piece in data[first_piece]:
                del data[first_piece][second_piece]
            elif isinstance(data[first_piece], list) and is_int(second_piece):
                list_idx = int(second_piece)

                data[first_piece].pop(list_idx)
            elif not ignore_invalid:
                raise InvalidSpecError(key=second_piece, data=data)
    elif len(pieces) > NESTED_PIECES_COUNT:
        next_piece_idx = spec.index(".") + 1
        remaining_spec = spec[next_piece_idx:]

        piece = pieces[0]
        remaining_data = data[piece]

        if isinstance(remaining_data, list):
            remaining_spec_pieces = remaining_spec.split(".")

            if len(remaining_spec_pieces) > 1 and is_int(remaining_spec_pieces[0]):
                list_idx = int(remaining_spec_pieces[0])

                remaining_data = remaining_data[list_idx]
                remaining_spec = ".".join(remaining_spec_pieces[1:])

        process(data=remaining_data, spec=remaining_spec, ignore_invalid=ignore_invalid)
