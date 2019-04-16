from typing import List

from ux.calcs.basic_calcs.task_success import binary_task_success_rate


class TaskResult(object):

    def __init__(self, value, metadata: dict = None):

        self.value = value
        self.metadata = metadata

    @staticmethod
    def binary_task_success_rate(results,
                                 alpha: float = 0.05, method: str = 'normal',
                                 name: str = None):
        """
        :type results: List[TaskResult]
        :param results: list of pass (1/True) / fail (0/False) results
        :param alpha: significance level
        :param method: method to use for confidence interval
        :param name: optional name
        :rtype: SuccessRate
        """
        result_values = [result.value for result in results]
        return binary_task_success_rate(
            results=result_values, alpha=alpha,
            method=method, name=name
        )


r1 = (0.5, {'task': 'task 1', 'user': 'user 1'})
r2 = (0.6, {'task': 'task 1', 'user': 'user 2'})
r3 = (0.7, {'task': 'task 2', 'user': 'user 1'})
r4 = (0.8, {'task': 'task 2', 'user': 'user 2'})


tr1 = TaskResult(*r1)
tr2 = TaskResult(*r2)
tr3 = TaskResult(*r3)
tr4 = TaskResult(*r4)
