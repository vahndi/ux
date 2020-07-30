from datetime import datetime, timedelta
from typing import List


class TimingFactory(object):

    @staticmethod
    def constant(start: datetime,
                 sources: List[str],
                 dwell: timedelta,
                 **kwargs) -> List[datetime]:
        """
        Return a list of constantly-spaced dwell-times starting at start.
        """
        date_times = []
        current_date_time = start
        for t in range(len(sources)):
            date_times.append(current_date_time)
            current_date_time += dwell
        return date_times

    @staticmethod
    def constant_per_action_type(start: datetime,
                                 action_types: List[str],
                                 dwell_times: dict,
                                 **kwargs) -> List[datetime]:
        """
        Return a list of times spaced based on the action type.
        """
        date_times = []
        current_date_time = start
        for a in range(len(action_types)):
            date_times.append(current_date_time)
            current_date_time += dwell_times[action_types[a]]
        return date_times

    @staticmethod
    def random_exponential(
            start: datetime, sources: List[str]
    ) -> List[datetime]:

        pass
