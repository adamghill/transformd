from mergedeep import Strategy, merge
from typeguard import typechecked

from transformd.utils import is_int


class InvalidSpecError(Exception):
    pass


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
            current_data = self.data
            piece_data = {}
            new_data = {}

            # Break the spec into a list based on dots
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

            # Specify the additive strategy so that nothing gets clobbered while merging
            merge(transformed_data, piece_data, strategy=Strategy.ADDITIVE)

        return transformed_data
