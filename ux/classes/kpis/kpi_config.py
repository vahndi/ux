from typing import Dict, List

from ux.custom_types import SequenceFilter


class KPIConfig(object):

    def __init__(self, name: str, condition: SequenceFilter,
                 numerator_splits: List[str], denominator_splits: List[str],
                 split_defs: Dict[str, Dict[str, SequenceFilter]] = None):
        """
        Configuration for calculating a KPI metric.

        :param name: Name for the configuration object.
        :param condition: SequenceFilter that must be True for the sequence to be included in the numerator.
        :param numerator_splits: List of splits to calculate numerators for.
        :param denominator_splits: List of splits to calculate denominators for.
        :param split_defs: Optional definitions of the numerator and denominator splits
                           in format dict[split_name, dict[sub_split_name, SequenceFilter]]
        """
        self.name = name
        self.condition = condition
        self.split_defs = split_defs
        self.numerator_splits = numerator_splits
        self.denominator_splits = denominator_splits
