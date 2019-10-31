import unittest
from unittest import TestCase

from ux.calcs.object_calcs.task_success import ordered_task_completion_rate, unordered_task_completion_rate
from ux.classes.sequences.action_sequence import ActionSequence
from ux.classes.actions.action_template import ActionTemplate
from ux.classes.tasks.task import Task
from ux.classes.actions.user_action import UserAction


class TestTaskSuccess(TestCase):

    def setUp(self):

        self.test_task = Task(
            name='OrderedTask',
            action_templates=[
                ActionTemplate(
                    action_type='test-action',
                    source_id='location-{}'.format(a + 1),
                ) for a in range(5)
            ]
        )
        self.ordered_test_sequence = ActionSequence(
            user_actions=[
                UserAction(
                    action_id='action-{}'.format(i),
                    action_type='test-action',
                    source_id='location-{}'.format(a),
                    time_stamp=None, user_id=None, session_id=None
                ) for i, a in enumerate([1, 2, 3, 2, 3, 4, 5])
            ]
        )
        self.unordered_test_sequence = ActionSequence(
            user_actions=[
                UserAction(
                    action_id='action-{}'.format(i),
                    action_type='test-action',
                    source_id='location-{}'.format(a),
                    time_stamp=None, user_id=None, session_id=None
                ) for i, a in enumerate([1, 2, 3, 2, 5, 4])
            ]
        )

    def test_ordered_task_completion_rate_1(self):

        self.assertEqual(
            1,
            ordered_task_completion_rate(
                task=self.test_task,
                action_sequence=self.ordered_test_sequence
            )
        )

    def test_ordered_task_completion_rate_2(self):

        self.assertEqual(
            0.8,
            ordered_task_completion_rate(
                task=self.test_task,
                action_sequence=self.unordered_test_sequence
            )
        )

    def test_unordered_task_completion_rate_1(self):

        self.assertEqual(
            1,
            unordered_task_completion_rate(
                task=self.test_task,
                action_sequence=self.ordered_test_sequence
            )
        )

    def test_unordered_task_completion_rate_2(self):

        self.assertEqual(
            1,
            unordered_task_completion_rate(
                task=self.test_task,
                action_sequence=self.unordered_test_sequence
            )
        )


if __name__ == '__main__':

    unittest.main()
