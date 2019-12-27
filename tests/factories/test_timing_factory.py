from datetime import datetime, timedelta
from unittest import TestCase

from ux.utils.factories.constants import SRCS_TGTS__ONE_SHOT__ABCDE
from ux.utils.factories.timing_factory import TimingFactory


class TestTimingFactory(TestCase):

    def setUp(self) -> None:

        self.y2k: datetime = datetime(2000, 1, 1, 0, 0, 0)

    def test_constant(self):

        action_dts = TimingFactory.constant(
            sources=SRCS_TGTS__ONE_SHOT__ABCDE,
            start=self.y2k,
            dwell=timedelta(seconds=1)
        )
        action_dts_ref = [
            datetime(2000, 1, 1, 0, 0, 0),
            datetime(2000, 1, 1, 0, 0, 1),
            datetime(2000, 1, 1, 0, 0, 2),
            datetime(2000, 1, 1, 0, 0, 3)
        ]
        self.assertEqual(action_dts, action_dts_ref)

    def test_constant_per_action_type(self):

        action_types = [
            'forward', 'forward', 'forward',
            'back', 'back',
            'forward', 'forward', 'forward'
        ]
        action_dts_ref = [
            datetime(2000, 1, 1, 0, 0, 0),
            datetime(2000, 1, 1, 0, 0, 1),
            datetime(2000, 1, 1, 0, 0, 2),
            datetime(2000, 1, 1, 0, 0, 3),
            datetime(2000, 1, 1, 0, 0, 5),
            datetime(2000, 1, 1, 0, 0, 7),
            datetime(2000, 1, 1, 0, 0, 8),
            datetime(2000, 1, 1, 0, 0, 9),
        ]
        dwell_times = {
            'forward': timedelta(seconds=1),
            'back': timedelta(seconds=2)
        }
        action_dts = TimingFactory.constant_per_action_type(
            action_types=action_types,
            start=self.y2k,
            dwell_times=dwell_times
        )
        self.assertEqual(action_dts, action_dts_ref)
