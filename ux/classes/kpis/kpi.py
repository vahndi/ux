from numpy import inf


class KPI(object):

    def __init__(self, name: str, numerator: int, denominator: int,
                 numer_config: dict = None, denom_config: dict = None):
        """
        Defines a KPI metric, typically expressed as a percentage of users who did something.

        :param numerator: The number of users who did something.
        :param denominator: The set of users who did or did not do the thing.
        :param numer_config: Optional dict[split_name, filter_name] of config params used to calculate the numerator.
        :param denom_config: Optional dict[split_name, filter_name] of config params used to calculate the denominator.
        """
        self.name = name
        self.numerator = numerator
        self.denominator = denominator
        self.numer_config = numer_config
        self.denom_config = denom_config

    @property
    def proportion(self):
        if self.denominator == 0:
            return inf
        return self.numerator / self.denominator

    @property
    def percentage(self):
        if self.denominator == 0:
            return inf
        return 100 * self.numerator / self.denominator

    def to_dict(self):
        """
        :rtype: Dict 
        """
        out_dict = {
            'name': self.name,
            'numerator': self.numerator,
            'denominator': self.denominator,
            'percentage': self.percentage,
            'proportion': self.proportion
        }
        if self.numer_config is not None:
            for k, v in self.numer_config.items():
                out_dict['numerator__' + k] = v
        if self.denom_config is not None:
            for k, v in self.denom_config.items():
                out_dict['denominator__' + k] = v
        return out_dict
