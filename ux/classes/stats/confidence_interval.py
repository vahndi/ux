class ConfidenceInterval(object):
    """
    Represents a confidence interval.
    """
    def __init__(self, lower: float, upper: float, significance: float):
        """
        Create a new confidence interval

        :param lower: Lower bound.
        :param upper: Upper bound.
        :param significance: Significance level (0 - 1).
        """
        self.lower = lower
        self.upper = upper
        self.significance = significance

    @property
    def percentage(self):
        """
        :rtype: float
        """
        return 100 * (1 - self.significance)

    @property
    def width(self):
        return self.upper - self.lower

    @property
    def range(self):
        return self.lower, self.upper
