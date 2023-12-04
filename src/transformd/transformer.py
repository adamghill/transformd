from typing import Union

from mergedeep import Strategy, merge
from typeguard import typechecked

from transformd.strategies import exclusion, inclusion


@typechecked
class Transformer:
    """Transforms a dictionary based on a `spec`."""

    def __init__(self, data: dict):
        """Creates a new transformer with the `dictionary` data to later be transformed."""

        self.data = data

    def _get_specs(self, spec: Union[str, tuple[str, ...], list[str]]) -> Union[tuple[str, ...], list[str]]:
        """Ensures that the passed-in spec is a list/tuple.

        Args:
            spec: The `dictionary` specification.

        Returns:
            A `spec` as a list/tuple.
        """

        if isinstance(spec, str):
            return [spec]

        return spec

    def transform(self, spec: Union[str, tuple[str, ...], list[str]], ignore_invalid: bool = False) -> dict:
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

                exclusion.process(data=excluded_data, spec=exclusion_spec, ignore_invalid=ignore_invalid)

                # Overwrite with the excluded data
                transformed_data = excluded_data
            else:
                included_data = inclusion.process(data=self.data, spec=spec, ignore_invalid=ignore_invalid)

                # Specify the additive strategy so that nothing gets clobbered while merging
                merge(
                    transformed_data,
                    included_data,
                    strategy=Strategy.ADDITIVE,
                )

        return transformed_data
