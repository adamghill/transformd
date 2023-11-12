from transformd.exceptions import InvalidSpecError
from transformd.utils import is_int


def process(data: dict, spec: str, ignore_invalid: bool = False) -> dict:
    """Handle inclusion specs, i.e. specs that specify which parts of the original dictionary to include
    in a new dictionary. This will be any spec that does not start with a dash.

    Args:
        spec: Specifies the data to return.
        ignore_invalid: Whether to ignore an invalid spec or not. Raises `InvalidSpecError`
            if `False` and the spec is invalid. Defaults to `False`.

    Returns:
        A `dictionary` with only the data that was specified in the spec.
    """

    piece_data = {}
    new_data = {}

    # Break the spec into a list of pieces based on dot notation
    pieces = spec.split(".")

    skip_idx = False

    if len(pieces) == 1:
        piece_data = new_data

    for idx, piece in enumerate(pieces):
        if skip_idx:
            skip_idx = False
            continue

        if piece in data and isinstance(data[piece], list) and len(pieces) >= idx + 2 and is_int(pieces[idx + 1]):
            # Handle this as referring to a list
            if piece not in new_data:
                new_data[piece] = []

            # Handle the nested attribute inside the list
            if len(pieces) >= idx + 3:
                # Create one object and use index of 0 here because `mergedeep`
                # will handle merging the nested lists together later
                new_data[piece].append({})
                new_data = new_data[piece][0]

                # Move the pointer to the object in the list
                list_idx = int(pieces[idx + 1])
                data = data[piece][list_idx]

                # Skip the next idx in the list because it specifies the index of the nested list
                # which is already handled above
                skip_idx = True
        elif len(pieces) == idx + 1 and is_int(piece):
            # Handles a list index, e.g. `books.0`

            list_piece = pieces[idx - 1]
            list_idx = int(piece)

            new_data[list_piece].append(data[list_piece][list_idx])
        elif piece in data:
            if idx == len(pieces) - 1:
                new_data.update({piece: data[piece]})
            else:
                new_data.update({piece: {}})

                if piece_data == {}:
                    piece_data.update(new_data)

                new_data = new_data[piece]
                data = data[piece]
        elif ignore_invalid is False:
            raise InvalidSpecError(key=piece, data=data)

    return piece_data
