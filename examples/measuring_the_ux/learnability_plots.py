import matplotlib.pyplot as plt
from numpy.random import randint

from plots.usability.learnability import plot_task_learnability


def time_on_task_over_trials():
    """
    Emulate the plot from Figure 4.5 of "Measuring the User Experience".
    """
    # generate example data
    task_time = {
        'Trial 1': randint(60, 80, size=10),
        'Trial 2': randint(50, 70, size=10),
        'Trial 3': randint(50, 60, size=10),
        'Trial 4': randint(40, 50, size=10),
        'Trial 5': randint(40, 45, size=10),
        'Trial 6': randint(35, 40, size=10),
        'Trial 7': randint(30, 40, size=10)
    }
    # plot
    plot_task_learnability(task_time)
    plt.show()


if __name__ == '__main__':

    time_on_task_over_trials()

