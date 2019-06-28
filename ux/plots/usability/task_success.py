from collections import OrderedDict
from matplotlib.axes import Axes
from numpy import array, ndarray, histogram
from pandas import DataFrame, Series
from typing import Union, Iterable

from ux.calcs.basic_calcs.task_success import binary_task_success_rate
from ux.plots.helpers import new_axes, get_hist_index


def plot_task_success_rates(task_results: dict, ax: Axes = None):
    """
    Plot a bar plot of success rates on several tasks.

    :param task_results: Dictionary {task_name => task results list}.
    :param ax: Optional matplotlib axes.
    :rtype: Axes
    """
    # calculate plot data
    # TODO: debug confidence interval to match the book
    success_rates = {
        task_name: binary_task_success_rate(task_results[task_name])
        for task_name in task_results.keys()
    }
    means = Series({
        task_name: success_rates[task_name][0]
        for task_name in success_rates.keys()
    })
    confidence_intervals = array([
        success_rates[task_name][1]
        for task_name in means.index
    ])
    errors = confidence_intervals.copy()
    errors[:, 0] = means - errors[:, 0]
    errors[:, 1] = errors[:, 1] - means
    errors = errors.reshape(1, 2, means.shape[0])
    ax = ax or new_axes()
    means *= 100
    errors *= 100
    means.plot(kind='bar', ax=ax, yerr=errors, capsize=5)
    ax.set_xlabel('Task')
    ax.set_ylabel('% Successful')
    ax.set_ylim(0, 105)
    return ax


def plot_task_success_frequencies(
        success_rates, bins: Union[list, range] = None,
        ax: Axes = None
):
    """
    Plot frequencies of success rates for one or many scenarios.

    :param success_rates: List of success rates for one scenario, or dict(name->success_rates) for many.
    :type success_rates: Union[List[float], Dict[str, List[float]]]
    :param bins: Bins for the histogram calculation.
    :param ax: Optional matplotlib axes.
    :rtype: Axes
    """
    bins = bins or range(0, 110, 10)
    if type(success_rates) in [ndarray, list]:
        means = Series(
            data=success_rates,
            name='Success Rate'
        )
        means *= 100
        hist = Series(histogram(means, bins=bins)[0])
        hist.index = get_hist_index(bins)
        ax = ax or new_axes()
        hist.plot(kind='bar', ax=ax)
        ax.set_xlabel('Success Rate')
        ax.set_ylabel('Frequency')
        return ax
    elif type(success_rates) in (dict, OrderedDict):
        means_dict = dict()
        for name in success_rates.keys():
            means = array(success_rates[name])
            means *= 100
            means_dict[name] = histogram(means, bins=bins)[0]
        df = DataFrame(means_dict)
        df.index = get_hist_index(bins)
        ax = ax or new_axes()
        df.plot(kind='bar', ax=ax)
        ax.set_xlabel('Success Rate')
        ax.set_ylabel('Frequency')
        return ax
    else:
        raise TypeError


def plot_task_completion_rates(completion_rates, bins: Union[list, range] = None,
                               ax: Axes = None):

    """
    Plot rate of task completion for a given task.

    :param completion_rates: Completion rates for each participant (0 - 1)
    :type completion_rates: Union[List[float], Dict[str, List[float]]]
    :param bins: Bins for the histogram calculation.
    :param ax: Optional matplotlib axes.
    :rtype: Axes
    """
    ax = ax or new_axes()
    bins = bins or range(0, 110, 10)
    hist_index = get_hist_index(bins)

    def get_hist_series(rates: list):
        rates = Series(rates)
        rates *= 100
        hist = Series(histogram(rates, bins=bins)[0])
        hist.index = hist_index
        return hist

    if type(completion_rates) is list:
        data = get_hist_series(completion_rates)
    elif type(completion_rates) in (dict, OrderedDict):
        data = DataFrame({
            k: get_hist_series(rates=v)
            for k, v in completion_rates.items()
        })
    else:
        raise TypeError

    data.plot(kind='bar', ax=ax)
    ax.set_xlabel('Completion Rate')
    ax.set_ylabel('Frequency')


def plot_task_success_level(task_results: dict,
                            bar_order: Iterable[str] = None,  colors: Iterable[str] = None,
                            ax: Axes = None):
    """
    Plot a stacked bar chart of levels of success over different tasks.

    :param task_results: Dictionary {task name => {LoS => num participants})
    :param ax: Optional matplotlib axes.
    :rtype: Axes
    """
    df = DataFrame.from_dict(task_results, orient='index')
    df_percent = df.apply(lambda x: 100 * x / x.sum(), axis=1)
    ax = ax or new_axes()
    if bar_order is not None:
        df_percent = df_percent[bar_order]
    df_percent.plot(kind='bar', stacked=True, ax=ax, color=colors)
    ax.set_xlabel('Task')
    ax.set_ylabel('% of Participants')
    return ax
