import matplotlib.pyplot as plt

from plots.usability.errors import plot_percentage_task_errors


def percentage_task_errors():
    """
    Emulate the plot from Figure 4.8 of "Measuring the User Experience".
    """
    # generate example data
    condition_result = {
        'Control': [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1],
        'Condition 1': [1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
        'Condition 2': [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0],
        'Condition 3': [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        'Condition 4': [0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
        'Condition 5': [0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        'Condition 6': [0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
        'Condition 7': [0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
        'Condition 8': [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1]
    }
    # plot
    plot_percentage_task_errors(condition_result)
    plt.show()


if __name__ == '__main__':

    percentage_task_errors()
