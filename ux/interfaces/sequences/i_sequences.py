from datetime import timedelta, datetime
from typing import Dict, Iterator, List, Union, Tuple, Counter

from ux.classes.wrappers.map_result import MapResult
from ux.custom_types.builtin_types import StrPair
from ux.interfaces.actions.i_action_template import IActionTemplate
from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.sequences.i_sequences_group_by import ISequencesGroupBy


class ISequences(object):

    @property
    def sequences(self) -> List[IActionSequence]:
        """
        Return a list of the individual Sequences in the collection.
        """
        raise NotImplementedError

    def filter(self, condition) -> 'ISequences':

        raise NotImplementedError

    def chain_filter(self, filters) -> 'ISequencesGroupBy':
        """
        Return a new SequencesGroupBy keyed by the dict key with values matching each filter, applied in series.

        :param filters: Dictionary of filters to apply. Use OrderedDict for Python < 3.7 to preserve key order.
        """
        raise NotImplementedError

    def group_filter(self, filters, group_name: str = 'filter') -> 'ISequencesGroupBy':

        raise NotImplementedError

    def count(self, condition=None) -> int:

        raise NotImplementedError

    def counter(self, get_value) -> Counter:
        """
        Return a dict of counts of each value returned by get_value(action) for each action.

        :param get_value: method that returns a str or list of strs when called on an action.
        """
        raise NotImplementedError

    def copy(self) -> 'ISequences':

        raise NotImplementedError

    def intersection(self, other) -> 'ISequences':

        raise NotImplementedError

    @staticmethod
    def intersect_all(sequences: List['ISequences']) -> 'ISequences':

        raise NotImplementedError

    def back_click_rates(self) -> Dict[IActionTemplate, float]:

        raise NotImplementedError

    def group_by(self, by) -> 'ISequencesGroupBy':

        raise NotImplementedError

    @property
    def metas(self) -> List[dict]:
        raise NotImplementedError

    @property
    def starts(self) -> List[datetime]:
        raise NotImplementedError

    @property
    def ends(self) -> List[datetime]:
        raise NotImplementedError

    @property
    def durations(self) -> List[timedelta]:
        raise NotImplementedError

    @property
    def user_ids(self) -> List[str]:
        raise NotImplementedError

    @property
    def session_ids(self) -> List[str]:
        raise NotImplementedError

    def action_template_counts(self) -> Dict[IActionTemplate, int]:

        raise NotImplementedError

    def action_template_sequence_counts(self) -> Dict[IActionTemplate, int]:
        """
        Return a total count of the number of ActionSequences containing each ActionTemplate in the collection.
        """
        raise NotImplementedError

    def action_template_transition_counts(self) -> Dict[Tuple[IActionTemplate, IActionTemplate], int]:
        """
        Return counts of transitions between pairs of Actions from each Sequence in the collection.

        :return: Dictionary of {(from, to) => count}
        """
        raise NotImplementedError

    def location_transition_counts(self, exclude=None) -> Counter[StrPair]:
        """
        Count the transitions from each location to each other location in actions in the given sequences.

        :return: Counter[Tuple[from, to], count]
        """
        raise NotImplementedError

    def dwell_times(self, sum_by_location: bool, sum_by_sequence: bool) -> Dict[str, Union[timedelta, List[timedelta]]]:
        """
        Return the amount of time spent by the user at each location.

        :param sum_by_location: Whether to sum the durations of time spent at each location or keep as a list.
        :param sum_by_sequence: Whether to sum the durations of time spent at each location in each sequence or keep as a list.
        """
        raise NotImplementedError

    def map(self, mapper) -> MapResult:

        raise NotImplementedError

    def sort(self, by: str, ascending: bool = True) -> 'ISequences':

        raise NotImplementedError

    def __getitem__(self, value):

        raise NotImplementedError

    def __len__(self) -> int:

        raise NotImplementedError

    def __contains__(self, item: IActionSequence) -> bool:

        raise NotImplementedError

    def __iter__(self) -> Iterator[IActionSequence]:

        raise NotImplementedError

    def __add__(self, other: 'ISequences') -> 'ISequences':

        raise NotImplementedError

    def __sub__(self, other: 'ISequences') -> 'ISequences':

        raise NotImplementedError
