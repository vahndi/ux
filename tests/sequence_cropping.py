from datetime import datetime

from ux.classes.actions.user_action import UserAction
from ux.classes.sequences.action_sequence import ActionSequence

a = UserAction(
    action_id='1',
    action_type='a',
    source_id='a',
    time_stamp=datetime.now(),
    user_id='1', session_id='1'
)
b = UserAction(
    action_id='1',
    action_type='b',
    source_id='b',
    time_stamp=datetime.now(),
    user_id='1', session_id='1'
)
c = UserAction(
    action_id='1',
    action_type='c',
    source_id='c',
    time_stamp=datetime.now(),
    user_id='1', session_id='1'
)
d = UserAction(
    action_id='1',
    action_type='d',
    source_id='d',
    time_stamp=datetime.now(),
    user_id='1', session_id='1'
)

seq = ActionSequence(
    user_actions=[a, b, c, a, a, b, a, c, d]
)

crop_seq = seq.crop(start=a.template(), end=c.template(), how='first')
print(crop_seq)
crop_seq = seq.crop(start=a.template(), end=c.template(), how='last')
print(crop_seq)
crop_seq = seq.crop(start=a.template(), end=b.template(), how='first')
print(crop_seq)
crop_seq = seq.crop(start=a.template(), end=b.template(), how='last')
print(crop_seq)
crop_seq = seq.crop(start=b.template(), end=c.template(), how='first')
print(crop_seq)
crop_seq = seq.crop(start=b.template(), end=c.template(), how='last')
print(crop_seq)
crop_seq = seq.crop(start=d.template(), end=a.template(), how='last')
print(crop_seq)
