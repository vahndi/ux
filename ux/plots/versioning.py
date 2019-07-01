from datetime import datetime
from matplotlib.axes import Axes

from ux.interfaces.i_database_manager import IDatabaseManager
from ux.plots.helpers import new_axes
from ux.utils.versioning import find_location_history


def plot_location_history(manager: IDatabaseManager, start: datetime = None, end: datetime = None, ax: Axes = None):
    """
    Plot the history of each Location's appearance in the set of logs in Manager.

    :param manager: Child of IDatabaseManager containing the logs to use.
    :param start: Optional start date-time to exclude older sessions.
    :param end: Optional end date-time to exclude newer sessions.
    :param ax: Optional matplotlib axes to plot on.
    :rtype: Axes
    """
    ax = ax or new_axes()
    history = find_location_history(manager=manager, start=start, end=end)
    locations = list(history.keys())
    for l, location in enumerate(locations):
        ax.scatter(
            x=history[location],
            y=[l] * len(history[location]),
            marker='.'
        )
    ax.set_yticks(range(1, len(locations)))
    ax.set_yticklabels(locations)
    if start:
        x_lim = ax.get_xlim()
        ax.set_xlim(start, x_lim[1])
    if end:
        x_lim = ax.get_xlim()
        ax.set_xlim(x_lim[0], end)

