from typing import Iterable

from ux.classes.stats.confidence_interval import ConfidenceInterval


class SuccessRate(object):

    def __init__(self, mean: float, confidence_interval: ConfidenceInterval,
                 name: str = None):

        self.mean = mean
        self.confidence_interval = confidence_interval
        self.name = name or ''

    def __str__(self):

        return 'Mean: {:.2f}, CI: {:.2f}'.format(
            self.mean, self.confidence_interval.width
        )

    @staticmethod
    def means(success_rates):
        """
        Return a list of the mean value of each success rate

        :type success_rates: Iterable[SuccessRate]
        :rtype: list
        """
        return [
            success_rate.mean for success_rate in success_rates
        ]

    @property
    def errors(self):
        """
        Return the lower and upper error of the confidence interval bounds from the mean.

        :rtype: Tuple[float, float]
        """
        return (
            self.mean - self.confidence_interval.lower,
            self.confidence_interval.upper - self.mean
        )
