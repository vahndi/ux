from datetime import datetime

from ux.interfaces.i_session import ISession


class Session(ISession):
    """
    Represents a single User Session.
    """
    def __init__(self, session_id: str, user_id: str,
                 start_time: datetime, end_time: datetime):
        """
        Create a new Session.

        :param session_id: The id of the Session.
        :param user_id: The id of the User whose Session this is.
        :param start_time: The start date-time of the Session.
        :param end_time: The end date-time of the Session.
        """
        self._session_id = session_id
        self._user_id = user_id or None
        self._start_time = start_time
        self._end_time = end_time

    @property
    def session_id(self):
        """
        Return the id of the Session.

        :rtype: str
        """
        return self._session_id

    @property
    def user_id(self):
        """
        Return the id of the Session's User.

        :rtype: str
        """
        return self._user_id

    @property
    def start_time(self):
        """
        Return the start date-time of the Session

        :rtype: datetime
        """
        return self._start_time

    @property
    def end_time(self):
        """
        Return the end date-time of the Session

        :rtype: datetime
        """
        return self._end_time

    def __repr__(self):

        return 'Session({})'.format(self._session_id)
