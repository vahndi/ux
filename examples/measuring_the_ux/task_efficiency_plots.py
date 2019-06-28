from collections import OrderedDict
import matplotlib.pyplot as plt
from numpy.random import random, normal
from numpy import add, min

from plots.usability.efficiency import plot_task_completion_efficiency


def task_success_per_time_unit():
    """
    Emulate the plot from Figure 4.12 of "Measuring the User Experience"
    """
    # generate example data
    success_task_per_minute = OrderedDict(
        ('Prototype {}'.format(i),
         add(normal(random() * 2, 0.5, 100),
             abs(min(normal(random() * 2, 0.5, 100)))))
        for i in range(1, 5)
    )
    # plot
    plot_task_completion_efficiency(success_task_per_minute)
    plt.show()


if __name__ == '__main__':

    task_success_per_time_unit()
