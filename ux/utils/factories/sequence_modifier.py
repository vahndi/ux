from random import randint, random

from ux.classes.actions.user_action import UserAction
from ux.classes.sequences.action_sequence import ActionSequence
from ux.interfaces.sequences.i_action_sequence import IActionSequence


class SequenceModifier(object):

    @staticmethod
    def insert_action_types_at_random(sequence: IActionSequence, num_insertions,
                                      action_type: str,
                                      min_gap_proportion: float = 0.25):

        user = sequence[0].user_id
        session = sequence[0].session_id
        insert_afters = []
        insert_times = []
        for _ in range(num_insertions):
            insert_after = randint(0, len(sequence) - 2)
            insert_afters.append(insert_after)
            random_num = random() * (1 - 2 * min_gap_proportion) + min_gap_proportion
            action_time = sequence[insert_after].time_stamp + random_num * (
                sequence[insert_after + 1].time_stamp - sequence[insert_after].time_stamp
            )
            insert_times.append(action_time)
        new_actions = []
        for a in range(len(sequence)):
            new_actions.append(sequence[a])
            for i in range(num_insertions):
                if insert_afters[i] == a:
                    new_actions.append(UserAction(
                        action_id='inserted_{}'.format(i),
                        action_type=action_type,
                        source_id=sequence[a].target_id,
                        time_stamp=insert_times[i],
                        user_id=user, session_id=session
                    ))
        return ActionSequence(user_actions=new_actions)
