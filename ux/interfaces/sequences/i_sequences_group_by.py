from typing import KeysView, ValuesView, List, ItemsView

from ux.classes.wrappers.map_result import MapResult


class ISequencesGroupBy(object):

    def count(self) -> MapResult:

        raise NotImplementedError

    def items(self) -> ItemsView:

        raise NotImplementedError

    def keys(self) -> KeysView:

        raise NotImplementedError

    def values(self) -> ValuesView:

        raise NotImplementedError

    @property
    def names(self) -> List[str]:

        raise NotImplementedError

    def map(self, mapper) -> MapResult:

        raise NotImplementedError

    def agg(self, agg_funcs) -> MapResult:
        """
        :param agg_funcs: dict mapping attributes to one or more aggregation functions e.g. duration -> np.median
        """
        raise NotImplementedError

    def filter(self, condition) -> 'ISequencesGroupBy':
        """
        Return a new Sequences containing only the sequences matching the `condition` in each group.

        :param condition: lambda(sequence) that returns True to include a sequence.
        """
        raise NotImplementedError

    def group_filter(self, filters, group_name=None) -> 'ISequencesGroupBy':
        """
        Return a new SequencesGroupBy keyed by the filter name with values matching each filter, applied in parallel.

        :param filters: Dictionary of filters to apply.
        :param group_name: Name to identify the filter group.
        """
        raise NotImplementedError

    def __getitem__(self, item):
        """
        :rtype: ISequences
        """
        raise NotImplementedError
