from matplotlib.axes import Axes
from numpy import array, stack
from pandas import Series

from ux.calcs.basic_calcs.task_success import binary_task_success_rate
from ux.plots.helpers import new_axes


def plot_percentage_task_errors(condition_result: dict, ax: Axes = None):
    """
    Plot the percentage of errors on completing a task, for one or more scenarios e.g. conditions.

    :param condition_result: Dictionary {condition_name => condition results list (0 = no errors & 1 = error)}.
    :param ax: Optional matplotlib axes.
    :rtype: Axes
    """
    # calculate error rate
    error_rates = {
        condition_name: binary_task_success_rate(condition_result[condition_name])
        for condition_name in condition_result.keys()
    }
    means = Series({
        condition_name: error_rates[condition_name][0]
        for condition_name in error_rates.keys()
    })
    confidence_intervals = array([
        error_rates[condition_name][1]
        for condition_name in means.index
    ])
    errors = confidence_intervals.copy()
    lower = array(means - errors[:, 0])
    upper = array(errors[:, 1] - means)
    errors = stack([lower, upper])
    ax = ax or new_axes()
    means *= 100
    errors *= 100
    means.plot(kind='bar', ax=ax, yerr=errors, capsize=5)
    ax.set_xlabel('Condition')
    ax.set_ylabel('% Login Attempts with Error(s)')
    return ax
