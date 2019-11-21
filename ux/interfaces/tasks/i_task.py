class ITask(object):

    @property
    def name(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def action_templates(self):
        """
        :rtype: List[IActionTemplate]
        """
        raise NotImplementedError

    def unordered_completion_rate(self, action_sequence):
        """
        :type action_sequence: IActionSequence
        :rtype: float
        """
        raise NotImplementedError

    def ordered_completion_rate(self, action_sequence):
        """
        :type action_sequence: IActionSequence
        :rtype: float
        """
        raise NotImplementedError

    def intersects_sequence(self, action_sequence):
        """
        :type action_sequence: IActionSequence
        :rtype: bool
        """
        raise NotImplementedError

    def __getitem__(self, item):
        """
        :rtype: IActionTemplate
        """
        raise NotImplementedError

    def __len__(self):
        """
        should return the  number of user actions
        """
        raise NotImplementedError

    def __contains__(self, item):

        raise NotImplementedError

    def __iter__(self):

        raise NotImplementedError
