from collections import OrderedDict
import matplotlib.pyplot as plt
from numpy.random import randint, normal
from pandas import DataFrame

from plots.usability.time_on_task import plot_task_completion_times, plot_task_completion_under_threshold


def mean_time_on_task():
    """
    Emulate the plot from Figure 4.5 of "Measuring the User Experience".
    """
    # generate example data
    task_time = OrderedDict(
        ('Task {}'.format(i), normal(randint(60, 100), 10, 100))
        for i in range(1, 11)
    )
    # plot
    plot_task_completion_times(task_time)
    plt.show()


def task_completion_under_threshold():
    """
    Emulate the plot from Figure 4.6 of "Measuring the User Experience".
    """
    # generate example data
    participant_times = {
       'P1': [259, 112, 135, 58, 8],
       'P2': [253, 64, 278, 160, 22],
       'P3': [42, 51, 60, 57, 26],
       'P4': [38, 108, 115, 146, 26],
       'P5': [33, 142, 66, 47, 38],
       'P6': [33, 54, 261, 26, 42],
       'P7': [36, 152, 53, 22, 44],
       'P8': [112, 65, 171, 133, 46],
       'P9': [29, 92, 147, 56, 56],
       'P10': [158, 113, 136, 83, 64],
       'P11': [24, 69, 119, 25, 68],
       'P12': [108, 50, 145, 15, 75],
       'P13': [110, 128, 97, 97, 78],
       'P14': [37, 66, 105, 83, 80],
       'P15': [116, 78, 40, 163, 100],
       'P16': [129, 152, 67, 168, 109],
       'P17': [31, 51, 51, 119, 116],
       'P18': [33, 97, 44, 81, 127],
       'P19': [75, 124, 286, 103, 236],
       'P20': [76, 62, 108, 185, 245]
    }
    df = DataFrame.from_dict(participant_times, orient='index')
    df.columns = ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5']
    participant_times = df.to_dict()
    # plot
    plot_task_completion_under_threshold(participant_times)
    plt.show()


if __name__ == '__main__':

    mean_time_on_task()
    task_completion_under_threshold()

