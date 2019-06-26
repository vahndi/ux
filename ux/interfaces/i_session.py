class ISession(object):

    @property
    def session_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def user_id(self):
        """
        :rtype: str
        """
        raise NotImplementedError

    @property
    def start_time(self):
        """
        :rtype: datetime
        """
        raise NotImplementedError

    @property
    def end_time(self):
        """
        :rtype: datetime
        """
        raise NotImplementedError
