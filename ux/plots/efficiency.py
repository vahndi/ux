from matplotlib.axes import Axes
from numpy import array, mean
from pandas import Series

from ux.calcs.basic_calcs.stats import normal_confidence_interval
from ux.plots.helpers import new_axes


def plot_task_completion_efficiency(success_task_per_minute: dict, confidence: float = 0.95, ax: Axes = None):
    """
    Plot the number of completed tasks per unit time for each scenario e.g. prototypes, designs.

    :param success_task_per_minute: Dictionary of {scenario name => list of number of successful tasks per minute}
    :param confidence: The confidence interval to use for error bars (0 - 1)
    :param ax: Optional matplotlib axes to plot on.
    :rtype: Axes
    """
    means = Series({
        prototype_name: mean(num_success)
        for prototype_name, num_success in success_task_per_minute.items()
    })
    errors = array([
        normal_confidence_interval(success_task_per_minute[prototype_name], confidence=confidence)
        for prototype_name in means.index
    ]).reshape(1, 2, means.shape[0])
    ax = ax or new_axes()
    means.plot(kind='bar', ax=ax, yerr=errors, capsize=5)
    ax.set_xlabel('Prototypes')
    ax.set_ylabel('Tasks Successfully Completed per Minute')

    return ax

