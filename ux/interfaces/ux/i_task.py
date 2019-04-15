class ITask(object):

    @property
    def name(self):
        raise NotImplementedError

    @property
    def action_templates(self):

        raise NotImplementedError

    def unordered_completion_rate(self, action_sequence):

        raise NotImplementedError

    def ordered_completion_rate(self, action_sequence):

        raise NotImplementedError

    def intersects_sequence(self, action_sequence):

        raise NotImplementedError
