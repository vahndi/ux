from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from types import FunctionType
from typing import Callable, List

from ux.classes.actions.user_action import UserAction
from ux.classes.sequences.action_sequence import ActionSequence
from ux.plots.transitions import plot_sequence_diagram
from ux.utils.factories.action_type_factory import ActionTypeFactory
from ux.utils.factories.constants import LOCS__A_TO_Z, LOCS__ABCDE
from ux.utils.factories.sequence_modifier import SequenceModifier
from ux.utils.factories.source_target_factory import SourceTargetFactory
from ux.utils.factories.timing_factory import TimingFactory


def generate_sequence(locations: List[str],
                      sources_targets: Callable,
                      action_types: Callable,
                      time_stamps: Callable,
                      user_id: str, session_id: str,
                      time_stamp_kwargs: dict = None) -> ActionSequence:
    """
    Generate an ActionSequence based on user-supplied parameters.

    :param locations: list of locations in order that they would be visited
    :param sources_targets: {function to generate a }list of tuples of (source, target) from the locations
    :param action_types: {function to generate a }list of action types of from the sources and targets
    :param time_stamps: {function to generate a }list of timestamps based on the sources, targets and action types
    :param time_stamp_kwargs: additional keyword arguments to send to the time_stamps function
    :param user_id: the unique id of the user
    :param session_id: the unique id of the session
    """
    if isinstance(sources_targets, FunctionType):
        sources_targets = sources_targets(locations)
    source_ids = [st[0] for st in sources_targets]
    target_ids = [st[1] for st in sources_targets]
    if isinstance(action_types, FunctionType):
        action_types = action_types(sources=source_ids, targets=target_ids)
    if isinstance(time_stamps, FunctionType):
        if time_stamp_kwargs is None:
            time_stamp_kwargs = {}
        time_stamps = time_stamps(
            start=datetime(2000, 1, 1),
            sources=source_ids, targets=target_ids, action_types=action_types,
            **time_stamp_kwargs
        )
    action_ids = [str(i) for i in range(len(sources_targets))]
    actions = [
        UserAction(
            action_id=action_id,
            action_type=action_type,
            source_id=source_id, target_id=target_id,
            time_stamp=dt, user_id=user_id, session_id=session_id
        ) for action_id, action_type, source_id, target_id, dt in zip(
            action_ids, action_types, source_ids, target_ids, time_stamps
        )
    ]
    return ActionSequence(user_actions=actions)


if __name__ == '__main__':

    seq = generate_sequence(
        locations=LOCS__ABCDE,
        sources_targets=lambda locs: SourceTargetFactory.forward_back(locs, 3, 2),
        action_types=ActionTypeFactory.page_view__back_click,
        time_stamps=TimingFactory.constant_per_action_type,
        time_stamp_kwargs=dict(
            dwell_times={'page-view': timedelta(seconds=1),
                         'back-click': timedelta(seconds=2)}
        ),
        user_id='user_1',
        session_id='session_1'
    )
    seq = SequenceModifier.insert_action_types_at_random(
        sequence=seq, num_insertions=3, action_type='button-click'
    )
    ax = plot_sequence_diagram(seq, LOCS__ABCDE)
    plt.show()
