from typing import Iterable, List

from ux.classes.stats.confidence_interval import ConfidenceInterval
from ux.custom_types.builtin_types import FloatPair


class SuccessRate(object):
    """
    Represents a Task Success Rate.
    """
    def __init__(self, mean: float, confidence_interval: ConfidenceInterval,
                 name: str = None):
        """
        Create a new SuccessRate.

        :param mean: The mean value of the results.
        :param confidence_interval: The confidence interval of the results.
        :param name: The name for the SuccessRate.
        """
        self.mean: float = mean
        self.confidence_interval: ConfidenceInterval = confidence_interval
        self.name: str = name or ''

    def __str__(self) -> str:

        return 'Mean: {:.2f}, CI: {:.2f}'.format(
            self.mean, self.confidence_interval.width
        )

    @staticmethod
    def means(success_rates) -> List[float]:
        """
        Return a list of the mean value of each SuccessRate.

        :type success_rates: Iterable[SuccessRate]
        """
        return [
            success_rate.mean for success_rate in success_rates
        ]

    @property
    def errors(self) -> FloatPair:
        """
        Return the lower and upper error of the confidence interval bounds from the mean.
        """
        return (
            self.mean - self.confidence_interval.lower,
            self.confidence_interval.upper - self.mean
        )
