from datetime import datetime
from matplotlib.axes import Axes

from ux.database_manager import DatabaseManager
from ux.plots.helpers import new_axes
from ux.utils.versioning import find_location_history, find_action_type_history


def plot_history(manager: DatabaseManager,
                 start: datetime = None, end: datetime = None,
                 history_type: str = 'location', ax: Axes = None) -> Axes:
    """
    Plot the history of each Location's appearance in the set of logs in Manager.

    :param manager: Child of IDatabaseManager containing the logs to use.
    :param start: Optional start date-time to exclude older sessions.
    :param end: Optional end date-time to exclude newer sessions.
    :param history_type: Type of history to plot. One of ['location', 'action-type'].
    :param ax: Optional matplotlib axes to plot on.
    """
    ax = ax or new_axes()
    if history_type == 'location':
        find_history = find_location_history
    elif history_type == 'action-type':
        find_history = find_action_type_history
    else:
        raise ValueError("history_type must be 'location' or 'action-type'")
    history = find_history(manager=manager, start=start, end=end)
    locations = list(history.keys())
    # sort locations by first session
    locations = sorted(locations, key=lambda loc: history[loc][0])
    # plot histories
    for i_loc, location in enumerate(locations):
        color = 'C{}'.format(i_loc % 10)
        ax.scatter(
            x=history[location],
            y=[i_loc] * len(history[location]),
            marker='x', s=5, c=color
        )
        x = [history[location][0], history[location][-1]]
        y = [i_loc, i_loc]
        ax.plot(x, y, c=color, alpha=0.1)
    # format axes
    ax.set_yticks(range(1, len(locations)))
    ax.set_yticklabels(locations)
    if start:
        x_lim = ax.get_xlim()
        ax.set_xlim(start, x_lim[1])
    if end:
        x_lim = ax.get_xlim()
        ax.set_xlim(x_lim[0], end)

    return ax
