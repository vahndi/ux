from typing import Iterable

from numpy import mean, std
from scipy.stats import norm, expon


def normal_confidence_interval(data: Iterable, confidence: float = 0.95):
    """
    Compute confidence interval for array or list which is assumed to be normally distributed.

    :param data: list or array
    :param confidence: confidence level between 0 and 1
    :rtype: Tuple[float, float]
    """
    mu, sigma = mean(data), std(data, ddof=1)
    lower, upper = norm.interval(confidence, loc=mu, scale=sigma)
    error_lower = mu - lower
    error_upper = upper - mu
    return error_lower, error_upper


def exponential_confidence_interval(data: Iterable, confidence: float = 0.95):
    """
    Compute confidence interval for array or list which is assumed to be exponentially distributed.

    :param data: list or array
    :param confidence: confidence level between 0 and 1
    :rtype: Tuple[float, float]
    """
    shift, mu = expon.fit(data)
    interval = expon.interval(alpha=1-confidence, loc=shift, scale=mu)
    return mu - interval[0], interval[1] - mu