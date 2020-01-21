import unittest
from datetime import datetime, timedelta
from unittest import TestCase

from ux.calcs.object_calcs.time_on_task import task_extents
from ux.sequences import ActionSequence
from ux.actions.action_template import ActionTemplate
from ux.tasks import Task
from ux.actions.user_action import UserAction


class TestTimeOnTask(TestCase):

    def setUp(self) -> None:

        self.test_task: Task = Task(
            name='TestTask',
            action_templates=[
                ActionTemplate(action_type='action', source_id='location-1'),
                ActionTemplate(action_type='action', source_id='location-2'),
                ActionTemplate(action_type='action', source_id='location-3')
            ]
        )
        y2k = datetime(2000, 1, 1)
        self.test_actions: ActionSequence = ActionSequence(
            user_actions=[
                UserAction(action_id='1', action_type='action', source_id='location-A',
                           time_stamp=y2k, user_id='user_1', session_id='session_1'),
                UserAction(action_id='2', action_type='action', source_id='location-1',
                           time_stamp=y2k + timedelta(seconds=1), user_id='user_1', session_id='session_1'),
                UserAction(action_id='3', action_type='action', source_id='location-2',
                           time_stamp=y2k + timedelta(seconds=2), user_id='user_1', session_id='session_1'),
                UserAction(action_id='5', action_type='action', source_id='location-B',
                           time_stamp=y2k + timedelta(seconds=3), user_id='user_1', session_id='session_1'),
                UserAction(action_id='4', action_type='action', source_id='location-3',
                           time_stamp=y2k + timedelta(seconds=4), user_id='user_1', session_id='session_1'),
                UserAction(action_id='5', action_type='action', source_id='location-C',
                           time_stamp=y2k + timedelta(seconds=5), user_id='user_1', session_id='session_1')
            ]
        )

    def test_task_extents(self):

        self.assertEqual(
            (1, 4),
            task_extents(self.test_actions, self.test_task)
        )


if __name__ == '__main__':

    unittest.main()
