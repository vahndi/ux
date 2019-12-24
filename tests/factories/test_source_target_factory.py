from unittest import TestCase

from ux.utils.factories.constants import LOCS__ABCDE, SRCS_TGTS__ONE_SHOT__ABCDE, SRCS_TGTS__FORWARD_BACK__ABCDE
from ux.utils.factories.source_target_factory import SourceTargetFactory


class TestLocationFactory(TestCase):

    def test_one_shot(self):

        self.assertEqual(
            SourceTargetFactory.one_shot(LOCS__ABCDE),
            SRCS_TGTS__ONE_SHOT__ABCDE
        )

    def test_forward_back(self):

        self.assertEqual(
            SourceTargetFactory.forward_back(LOCS__ABCDE, 3, 2),
            SRCS_TGTS__FORWARD_BACK__ABCDE
        )
