class IUser(object):

    @property
    def user_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def session_ids(self):
        """
        :rtype: List[str]
        """
        raise NotImplementedError

    @property
    def action_ids(self):
        """
        :rtype: List[str]
        """
        raise NotImplementedError

    def add_action_id(self, action_id):
        raise NotImplementedError

    def add_session_id(self, session_id):
        raise NotImplementedError
