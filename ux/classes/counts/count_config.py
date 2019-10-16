from typing import List


class CountConfig(object):

    def __init__(self, name: str,
                 sequence_condition: callable = None,
                 sequence_split_by: callable = None,
                 action_condition: callable = None,
                 action_split_by: callable = None):

        self.name = name
        self.sequence_condition = sequence_condition
        self.sequence_split_by = sequence_split_by
        self.action_condition = action_condition
        self.action_split_by = action_split_by
