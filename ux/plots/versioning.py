from matplotlib.axes import Axes

from ux.interfaces.i_database_manager import IDatabaseManager
from ux.plots.helpers import new_axes
from ux.utils.versioning import find_location_history


def plot_location_history(manager: IDatabaseManager, ax: Axes = None):
    """
    Plot the history of each Location's appearance in the set of logs in Manager.

    :param manager: Child of IDatabaseManager containing the logs to use.
    :param ax: Optional matplotlib axes to plot on.
    :rtype: Axes
    """
    ax = ax or new_axes()
    history = find_location_history(manager)
    for l, location in enumerate(history.keys()):
        ax.scatter(
            x=history[location],
            y=[l] * len(history[location]),
        )
