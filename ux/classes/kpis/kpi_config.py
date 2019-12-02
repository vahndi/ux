from typing import Dict, List

from ux.custom_types import SequenceFilter


class KPIConfig(object):

    def __init__(self, name: str, condition: SequenceFilter,
                 numerator_splits: List[str] = None, denominator_splits: List[str] = None,
                 split_defs: Dict[str, Dict[str, SequenceFilter]] = None):
        """
        Configuration for calculating a collection of KPI metrics. Used in kpis.calculate_kpis_by_config.
        KPIs should be calculated for each combination of split_defs values pointed to by numerator_splits.
        Denominator splits must be a subset of numerator splits. Each value of the split_def in the numerator will be
        divided by its associated denominator value.

        :param name: Name for the configuration object.
        :param condition: SequenceFilter that must be True for the sequence to be included in the numerator.
        :param numerator_splits: List of names of splits to calculate numerators for.
        :param denominator_splits: List of names of splits to calculate denominators for.
        :param split_defs: Optional definitions of the numerator and denominator splits
                           in format dict[split_name, dict[sub_split_name, SequenceFilter]]
        """
        self.name = name
        self.condition = condition
        self.split_defs = split_defs
        self.numerator_splits = numerator_splits or []
        self.denominator_splits = denominator_splits or []
