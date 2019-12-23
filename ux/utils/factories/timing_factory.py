from datetime import datetime, timedelta
from typing import List, Tuple


def constant(sources_targets: List[Tuple[str, str]],
             start: datetime, dwell: timedelta) -> List[datetime]:
    """
    Return a list of constantly-spaced dwell-times starting at start.
    """
    date_times = []
    current_date_time = start
    for t in range(len(sources_targets)):
        date_times.append(current_date_time)
        current_date_time += dwell
    return date_times


def constant_per_action_type(action_types: List[str],
                             start: datetime, dwell_times: dict) -> List[datetime]:
    """
    Return a list of times spaced based on the action type.
    """
    date_times = []
    current_date_time = start
    for a in range(len(action_types)):
        date_times.append(current_date_time)
        current_date_time += dwell_times[action_types[a]]
    return date_times


if __name__ == '__main__':

    s_t = [('a', 'b'),
           ('b', 'c'),
           ('c', 'd'),
           ('d', 'e'),
           ('e', 'f')]
    for dt in constant(sources_targets=s_t,
                       start=datetime.now(),
                       dwell=timedelta(seconds=15)):
        print(dt)
