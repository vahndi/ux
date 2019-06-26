import unittest
from unittest import TestCase

from ux.calcs.object_calcs.time_on_task import task_extents
from ux.classes.actions.action_sequence import ActionSequence
from ux.classes.actions.action_template import ActionTemplate
from ux.classes.tasks.task import Task
from ux.classes.ux.user_action import UserAction


class TestTimeOnTask(TestCase):

    def setUp(self):

        self.test_task = Task(
            name='TestTask',
            action_templates=[
                ActionTemplate(action_type='action', source_id='location-1'),
                ActionTemplate(action_type='action', source_id='location-2'),
                ActionTemplate(action_type='action', source_id='location-3')
            ]
        )

        self.test_actions = ActionSequence(
            user_actions=[
                UserAction(action_id='1', action_type='action', source_id='location-A',
                           time_stamp=None, user_id=None, session_id=None),
                UserAction(action_id='2', action_type='action', source_id='location-1',
                           time_stamp=None, user_id=None, session_id=None),
                UserAction(action_id='3', action_type='action', source_id='location-2',
                           time_stamp=None, user_id=None, session_id=None),
                UserAction(action_id='5', action_type='action', source_id='location-B',
                           time_stamp=None, user_id=None, session_id=None),
                UserAction(action_id='4', action_type='action', source_id='location-3',
                           time_stamp=None, user_id=None, session_id=None),
                UserAction(action_id='5', action_type='action', source_id='location-C',
                           time_stamp=None, user_id=None, session_id=None)
            ]
        )

    def test_task_extents(self):

        self.assertEqual(
            (1, 4),
            task_extents(self.test_actions, self.test_task)
        )


if __name__ == '__main__':

    unittest.main()
