from typing import List, Tuple, Union

from mergedeep import Strategy, merge
from typeguard import typechecked

from transformd.utils import is_int, is_non_string_sequence


class DictionaryTransformer:
    @typechecked
    def __init__(self, data: dict):
        self.data = data

    @typechecked
    def transform(self, spec: Union[str, Tuple[str], List[str]]) -> dict:
        transformed_data = {}
        specs = []

        if is_non_string_sequence(spec):
            specs = spec
        else:
            specs = [spec]

        for field in specs:
            field_dict = {}

            sub_dict_data = self.data
            sub_dict = {}
            field_pieces = field.split(".")

            skip_idx = False

            if len(field_pieces) == 1:
                field_dict = sub_dict

            for idx, field_piece in enumerate(field_pieces):
                if skip_idx:
                    skip_idx = False
                    continue

                if (
                    field_piece in sub_dict_data
                    and isinstance(sub_dict_data[field_piece], list)
                    and len(field_pieces) >= idx + 2
                    and is_int(field_pieces[idx + 1])
                ):
                    # Handle this as referring to a list
                    if field_piece not in sub_dict:
                        sub_dict[field_piece] = []

                    # Handle the nested attribute inside the list
                    if len(field_pieces) >= idx + 3:
                        if field_dict == {}:
                            field_dict.update(sub_dict)

                        # Create one object and use index of 0 here because `mergedeep`
                        # will handle merging the nested lists together later
                        sub_dict[field_piece].append({})
                        sub_dict = sub_dict[field_piece][0]

                        # Move the pointer to the object in the list
                        list_idx = int(field_pieces[idx + 1])
                        sub_dict_data = sub_dict_data[field_piece][list_idx]

                        # Skip the next idx in the list because it specifies the index of the nested list
                        # which is already handled above
                        skip_idx = True
                elif len(field_pieces) == idx + 1 and is_int(field_piece):
                    # Handles a list index, e.g. `books.0`

                    list_field_piece = field_pieces[idx - 1]
                    list_idx = int(field_piece)

                    sub_dict[list_field_piece].append(
                        sub_dict_data[list_field_piece][list_idx]
                    )
                elif field_piece in sub_dict_data:
                    if idx == len(field_pieces) - 1:
                        sub_dict.update({field_piece: sub_dict_data[field_piece]})
                    else:
                        sub_dict.update({field_piece: {}})

                        if field_dict == {}:
                            field_dict.update(sub_dict)

                        sub_dict = sub_dict[field_piece]
                        sub_dict_data = sub_dict_data[field_piece]

            # Specify the additive strategy so that nothing gets clobbered while merging
            merge(transformed_data, field_dict, strategy=Strategy.ADDITIVE)

        return transformed_data
