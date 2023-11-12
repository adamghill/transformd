from mergedeep import Strategy, merge
from typeguard import typechecked

from transformd.utils import is_int


class InvalidSpecError(Exception):
    pass


NESTED_PIECES_COUNT = 2


@typechecked
class Transformer:
    """Transforms a dictionary based on a `spec`."""

    def __init__(self, data: dict):
        """Creates a new transformer with the `dictionary` data to later be transformed."""

        self.data = data

    def _get_specs(self, spec: str | tuple[str, ...] | list[str]) -> tuple[str, ...] | list[str]:
        """Ensures that the passed-in spec is a list/tuple.

        Args:
            spec: The `dictionary` specification.

        Returns:
            A `spec` as a list/tuple.
        """

        if isinstance(spec, str):
            return [spec]

        return spec

    def _process_exclusion_spec(self, data: dict, spec: str, ignore_invalid: bool = False) -> None:
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
                raise InvalidSpecError()

            del data[piece]
        elif len(pieces) == NESTED_PIECES_COUNT:
            (first_piece, second_piece) = pieces

            if first_piece not in data:
                raise InvalidSpecError()

            if data[first_piece] is not None:
                if second_piece in data[first_piece]:
                    del data[first_piece][second_piece]
                elif isinstance(data[first_piece], list) and is_int(second_piece):
                    list_idx = int(second_piece)

                    data[first_piece].pop(list_idx)
                elif not ignore_invalid:
                    raise InvalidSpecError()
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

            self._process_exclusion_spec(data=remaining_data, spec=remaining_spec, ignore_invalid=ignore_invalid)

    def _process_inclusion_spec(self, spec: str, ignore_invalid: bool = False) -> dict:
        """Handle inclusion specs, i.e. specs that specify which parts of the original dictionary to include
        in a new dictionary. This will be any spec that does not start with a dash.

        Args:
            spec: Specifies the data to return.
            ignore_invalid: Whether to ignore an invalid spec or not. Raises `InvalidSpecError`
                if `False` and the spec is invalid. Defaults to `False`.

        Returns:
            A `dictionary` with only the data that was specified in the spec.
        """

        current_data = self.data
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

            if (
                piece in current_data
                and isinstance(current_data[piece], list)
                and len(pieces) >= idx + 2
                and is_int(pieces[idx + 1])
            ):
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
                    current_data = current_data[piece][list_idx]

                    # Skip the next idx in the list because it specifies the index of the nested list
                    # which is already handled above
                    skip_idx = True
            elif len(pieces) == idx + 1 and is_int(piece):
                # Handles a list index, e.g. `books.0`

                list_piece = pieces[idx - 1]
                list_idx = int(piece)

                new_data[list_piece].append(current_data[list_piece][list_idx])
            elif piece in current_data:
                if idx == len(pieces) - 1:
                    new_data.update({piece: current_data[piece]})
                else:
                    new_data.update({piece: {}})

                    if piece_data == {}:
                        piece_data.update(new_data)

                    new_data = new_data[piece]
                    current_data = current_data[piece]
            elif ignore_invalid is False:
                raise InvalidSpecError(f"'{piece}' is invalid")

        return piece_data

    def transform(self, spec: str | tuple[str, ...] | list[str], ignore_invalid: bool = False) -> dict:
        """Transforms a dictionary based on a `spec` to keep the same "shape" of the original dictionary,
        but only include the pieces of the dictionary that are specified with dot-notation.

        Args:
            spec: Specifies the parts of the `dictionary` to keep.
            ignore_invalid: Whether to ignore an invalid spec or not. Raises `InvalidSpecError`
                if `False` and the spec is invalid. Defaults to `False`.

        Returns:
            A new `dictionary` with the specified shape based on the passed-in `spec`.
        """

        transformed_data = {}
        specs = self._get_specs(spec)

        for spec in specs:
            if spec.startswith("-"):
                exclusion_spec = spec[1:]
                excluded_data = transformed_data or self.data

                self._process_exclusion_spec(data=excluded_data, spec=exclusion_spec, ignore_invalid=ignore_invalid)

                # Overwrite with the excluded data
                transformed_data = excluded_data
            else:
                included_data = self._process_inclusion_spec(spec=spec, ignore_invalid=ignore_invalid)

                # Specify the additive strategy so that nothing gets clobbered while merging
                merge(
                    transformed_data,
                    included_data,
                    strategy=Strategy.ADDITIVE,
                )

        return transformed_data
