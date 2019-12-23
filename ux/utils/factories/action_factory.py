from typing import Callable, List

from ux.utils.factories.location_factory import one_shot
from ux.interfaces.actions.i_user_action import IUserAction


def one_shot_action_sequence(user_id: str, session_id: str, src_tgt_gen: Callable) -> List[IUserAction]:

    srcs_tgts = one_shot()
