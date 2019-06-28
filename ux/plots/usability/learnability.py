from matplotlib.axes import Axes
from numpy import mean
from pandas import Series

from ux.plots.helpers import new_axes


def plot_task_learnability(task_times: dict, ax: Axes = None):
    """
    Plot the change in time on task over a number of trials,

    :param task_times: Dictionary of {trial name => list of task times}
    :param ax: Optional matplotlib axes to plot on.
    :rtype: Axes
    """
    means = Series({
        trial_name: mean(times)
        for trial_name, times in task_times.items()
    })
    ax = ax or new_axes()
    means.plot(kind='line', ax=ax, marker="s")
    ax.set_xlabel('Trials')
    ax.set_ylabel('Time-on-Task (Sec')
    ax.set_ylim(0, 80)

    return ax
