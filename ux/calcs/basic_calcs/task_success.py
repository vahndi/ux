from typing import Iterable

from pandas import Series
from statsmodels.stats.proportion import proportion_confint


def binary_task_success_rate(results: Iterable[int],
                             alpha: float = 0.05, method: str = 'normal'):
    """
    Calculate the binary task success rate from a list of pass or fail task results for a given user.

    See http://www.statsmodels.org/devel/generated/statsmodels.stats.proportion.proportion_confint.html

    :param results: list of pass (1/True) / fail (0/False) results
    :param alpha: significance level
    :param method: method to use for confidence interval
    :rtype: SuccessRate
    """
    s: Series = Series(results).astype(int)
    mean = s.mean()
    confidence_interval = proportion_confint(
        count=s.sum(), nobs=s.shape[0],
        alpha=alpha, method=method

    )

    return mean, confidence_interval