from typing import Dict, List

from ux.custom_types import SequenceFilter, SequenceFilterSet


class KPIConfig(object):

    def __init__(self, name: str, condition: SequenceFilter,
                 numerator_sets: List[str] = None, denominator_sets: List[str] = None,
                 filter_sets: Dict[str, SequenceFilterSet] = None):
        """
        Configuration for calculating a collection of KPI metrics which use the same filter condition in the numerator
        but will be carried out for different subsequences depending on numerator and denominator filters.
        Used in kpis.calculate_kpis_by_config.

        :param name: Name for the configuration object.
        :param condition: SequenceFilter that must be True for the sequence to be included in the numerator.
        :param numerator_sets: List of names of SequenceFilterSets to calculate numerators for each SequenceFilter.
        :param denominator_sets: List of names of SequenceFilterSets to calculate denominators for each SequenceFilter.
        :param filter_sets: Optional definitions of the numerator and denominator SequenceFilterSets
                            in format dict[FilterSetName, dict[FilterName, SequenceFilter]]
        """
        self.name = name
        self.condition = condition
        self.numerator_sets = numerator_sets or []
        self.denominator_sets = denominator_sets or []
        self.filter_sets = filter_sets or []
