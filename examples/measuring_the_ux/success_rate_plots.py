from collections import OrderedDict
import matplotlib.pyplot as plt
from numpy.ma import clip
from numpy.random import normal

from plots.usability.task_success import (
    plot_task_success_rates, plot_task_success_frequencies, plot_task_success_level
)


def binary_success_rates():
    """
    Reproduce Figure 4.2 of "Measuring the User Experience".
    """
    # generate example data
    task_results = {
        'Task 1': [1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
        'Task 2': [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
        'Task 3': [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        'Task 4': [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        'Task 5': [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
    }
    # plot
    plot_task_success_rates(task_results)
    plt.show()


def binary_success_frequencies():
    """
    Emulate the plot from Figure 4.3 of "Measuring the User Experience".
    """
    # generate example data
    num_participants = 25
    mu_original = 0.65
    sigma_original = 0.2
    mu_redesign = 0.85
    sigma_redesign = 0.1
    samples_original = clip(normal(mu_original, sigma_original, num_participants), 0, 1)
    samples_redesign = clip(normal(mu_redesign, sigma_redesign, num_participants), 0, 1)
    success_rates = OrderedDict()
    success_rates['Original'] = samples_original
    success_rates['Redesign'] = samples_redesign
    bins = [0, 50, 60, 70, 80, 90, 100]
    # plot
    plot_task_success_frequencies(success_rates['Original'], bins=bins)
    plot_task_success_frequencies(success_rates, bins=bins)
    plt.show()


def success_level_distribution():
    """
    Emulate the plot from Figure 4.4 of "Measuring the User Experience".
    """
    # generate example data
    task_results = {
        'Task 1': {'Failure/quit': 20, 'Some problem': 30, 'No problem': 50},
        'Task 2': {'Failure/quit': 10, 'Some problem': 20, 'No problem': 70},
        'Task 3': {'Failure/quit': 40, 'Some problem': 50, 'No problem': 10},
        'Task 4': {'Failure/quit': 50, 'Some problem': 20, 'No problem': 30},
        'Task 5': {'Failure/quit': 10, 'Some problem': 10, 'No problem': 80}
    }
    # plot
    plot_task_success_level(task_results,
                            bar_order=['No problem', 'Some problem', 'No problem'],
                            colors=['#ccebc5', '#ffffcc', '#fbb4ae'])
    plt.show()


if __name__ == '__main__':

    binary_success_rates()
    binary_success_frequencies()
    success_level_distribution()
