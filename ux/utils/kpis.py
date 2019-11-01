from itertools import product
from typing import Dict, List

from ux.classes.kpis.kpi import KPI
from ux.classes.kpis.kpi_config import KPIConfig
from ux.interfaces.sequences.i_sequences import ISequences


def calculate_kpis_by_config(sequences: ISequences,
                             kpi_configs: List[KPIConfig],
                             split_defs: Dict[str, Dict[str, callable]]):
    """
    Calculate KPIs for a Sequences instance using a list of configurations.

    :param sequences: List of sequences that represent the population of user sessions to calculate from.
    :param kpi_configs: List of KPI Configurations to calculate KPIs with.
    :rtype: List[KPI]
    """
    # create subsets of sequences from kpi config split definitions
    sub_sequences = {}
    split_names = sorted(split_defs.keys())
    for filter_names in list(
            product(*[[None] + sorted(split_defs[split_name].keys())
                      for split_name in split_names])
    ):
        loop_seqs = sequences
        for split_name, filter_name in zip(split_names, filter_names):
            if filter_name is not None:
                loop_seqs = loop_seqs.filter(split_defs[split_name][filter_name])
        sub_sequences[filter_names] = loop_seqs
    # calculate kpis for each config
    results = []
    for kpi_config in kpi_configs:
        numerator_keys = list(product(*[[None] if split_name not in kpi_config.numerator_splits
                                        else sorted(split_defs[split_name].keys())
                                        for split_name in split_names]))
        denominator_keys = list(product(*[[None] if split_name not in kpi_config.denominator_splits
                                          else sorted(split_defs[split_name].keys())
                                          for split_name in split_names]))
        for numerator_key, denominator_key in product(numerator_keys, denominator_keys):
            if not all(
                numer == denom or denom is None
                for numer, denom in zip(numerator_key, denominator_key)
            ):
                continue
            numerator = sub_sequences[numerator_key].filter(kpi_config.condition).count()
            denominator = sub_sequences[denominator_key].count()
            results.append(KPI(
                name=kpi_config.name, numerator=numerator, denominator=denominator,
                numer_config={
                    split_name: numer_key_val
                    for split_name, numer_key_val in zip(split_names, numerator_key)
                    if numer_key_val is not None

                },
                denom_config={
                    split_name: denom_key_val
                    for split_name, denom_key_val in zip(split_names, denominator_key)
                    if denom_key_val is not None
                }
            ))
    return results
