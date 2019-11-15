from datetime import datetime

from ux.classes.actions.user_action import UserAction
from ux.classes.sequences.action_sequence import ActionSequence

s = UserAction(
    action_id='1',
    action_type='page-view',
    source_id='split-location',
    time_stamp=datetime.now(),
    user_id='1', session_id='1'
)
n = UserAction(
    action_id='2',
    action_type='page-view',
    source_id='non-split-location',
    time_stamp=datetime.now(),
    user_id='1', session_id='1'
)
seq_1 = ActionSequence([n, n, s, n, n, n, s])
seq_2 = ActionSequence([n, n, s, n, n, s, n])
seq_3 = ActionSequence([s, n, n, n, n, s, n])

for seq in (seq_1, seq_2, seq_3):
    print()
    print(seq)
    print()
    for split_seq in seq.split(s.template(), how='before'):
        print(split_seq)
    print()
    for split_seq in seq.split(s.template(), how='after'):
        print(split_seq)
    print()
    for split_seq in seq.split(s.template(), how='at'):
        print(split_seq)
