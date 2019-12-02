from itertools import product
from typing import Dict, List

from ux.classes.kpis.kpi import KPI
from ux.classes.kpis.kpi_config import KPIConfig
from ux.custom_types import SequenceFilterSet
from ux.interfaces.sequences.i_sequences import ISequences


def calculate_kpis_by_config(sequences: ISequences, kpi_configs: List[KPIConfig],
                             filter_sets: Dict[str, SequenceFilterSet]):
    """
    Calculate KPIs for a Sequences instance using a list of KPIConfigs.
    For each KPIConfig, KPIs will be calculated for each combination of filters pointed to by numerator_splits.
    Denominator splits must be a subset of numerator splits. Each value of the split_def in the numerator will be
    divided by its associated denominator value.

    :param sequences: List of sequences that represent the population of user sessions to calculate from.
    :param kpi_configs: List of KPI Configurations to calculate KPIs with.
    :param filter_sets: Dictionary mapping names of filter-sets to dictionaries of filter names to filter functions.
    :rtype: List[KPI]
    """
    # create sub-sequences from kpi config split definitions for product of split-definition values.
    sub_sequences = {}
    filter_set_names: List[str] = sorted(filter_sets.keys())
    for filter_names in list(
        product(*[[None] + sorted(filter_sets[filter_set_name].keys())
                  for filter_set_name in filter_set_names])
    ):
        loop_seqs = sequences
        for filter_set_name, filter_name in zip(filter_set_names, filter_names):
            if filter_name is not None:
                loop_seqs = loop_seqs.filter(filter_sets[filter_set_name][filter_name])
        sub_sequences[filter_names] = loop_seqs
    # calculate kpis for each config
    results = []
    for kpi_config in kpi_configs:
        # build products of filter name combinations for each split in the numerator and denominator
        numer_filter_product = list(product(*[[None] if split_name not in kpi_config.numerator_sets
                                            else sorted(filter_sets[split_name].keys())
                                            for split_name in filter_set_names]))
        denom_filter_product = list(product(*[[None] if split_name not in kpi_config.denominator_sets
                                            else sorted(filter_sets[split_name].keys())
                                            for split_name in filter_set_names]))
        # iterate over product of numerator and denominator filter combinations
        for numer_filter_names, denom_filter_names in product(numer_filter_product, denom_filter_product):
            # skip if any numerator and denominator filter names don't match
            if not all(
                numer_filter_name == denom_filter_name or denom_filter_name is None
                for numer_filter_name, denom_filter_name in zip(numer_filter_names, denom_filter_names)
            ):
                continue
            # create a new KPI for the combination of numerator and denominator filters
            numerator = sub_sequences[numer_filter_names].filter(kpi_config.condition).count()
            denominator = sub_sequences[denom_filter_names].count()
            results.append(KPI(
                name=kpi_config.name, numerator=numerator, denominator=denominator,
                numer_config={
                    filter_set_name: numer_filter_name
                    for filter_set_name, numer_filter_name in zip(filter_set_names, numer_filter_names)
                    if numer_filter_name is not None

                },
                denom_config={
                    filter_set_name: denom_filter_name
                    for filter_set_name, denom_filter_name in zip(filter_set_names, denom_filter_names)
                    if denom_filter_name is not None
                }
            ))
    return results
