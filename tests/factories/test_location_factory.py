from unittest import TestCase

from ux.utils.factories.constants import LOCS__ABCDE, SRCS_TGTS__ONE_SHOT__ABCDE, SRCS_TGTS__FORWARD_BACK__ABCDE
from ux.utils.factories.location_factory import one_shot, forward_back


class TestLocationFactory(TestCase):

    def test_one_shot(self):

        self.assertEqual(
            one_shot(LOCS__ABCDE),
            SRCS_TGTS__ONE_SHOT__ABCDE
        )

    def test_forward_back(self):

        self.assertEqual(
            forward_back(LOCS__ABCDE, 3, 2),
            SRCS_TGTS__FORWARD_BACK__ABCDE
        )
