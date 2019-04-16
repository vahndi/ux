from matplotlib.axes import Axes
from numpy import array, mean
from pandas import Series, DataFrame

from ux.calcs.basic_calcs.stats import exponential_confidence_interval
from ux.plots.helpers import new_axes


def plot_task_completion_times(task_times: dict, confidence: float = 0.95, ax: Axes = None):
    """
    Plot the average time taken and confidence interval for each task.

    :param task_times: Dictionary of {task name => list of task times}
    :param confidence: The confidence interval to use for error bars (0 - 1)
    :param ax: Optional matplotlib axes to plot on.
    :rtype: Axes
    """
    means = Series({
        task_name: mean(times)
        for task_name, times in task_times.items()
    })
    errors = array([
        exponential_confidence_interval(task_times[task_name], confidence=confidence)
        for task_name in means.index
    ]).reshape(1, 2, means.shape[0])
    ax = ax or new_axes()
    means.plot(kind='bar', ax=ax, yerr=errors, capsize=5)
    ax.set_xlabel('Task')
    ax.set_ylabel('Time (Sec) to Complete Task')

    return ax


def plot_task_completion_under_threshold(participant_times: dict, threshold: int = 60, ax: Axes = None):
    """
    Plot the percentage of participants who completed each task within the time threshold.

    :param participant_times: Dictionary mapping  {task name => {participant => time on task}}
    :param threshold: Time threshold to use to measure task completion success.
    :param ax: Optional matplotlib axes to plot on.
    :rtype: Axes
    """
    df = DataFrame.from_dict(participant_times)
    df_below_threshold = df.le(threshold).mean()
    ax = ax or new_axes()
    df_below_threshold.plot(kind='bar', ax=ax)
    ax.set_xlabel('Task')
    ax.set_ylabel('Participants')
    percents = ax.get_yticks()
    ax.set_yticklabels(['{:,.0%}'.format(percent) for percent in percents])
    return ax
