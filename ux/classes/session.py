from datetime import datetime


class Session(object):
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
        self._session_id: str = session_id
        self._user_id: str = user_id or None
        self._start_time: datetime = start_time
        self._end_time: datetime = end_time

    @property
    def session_id(self) -> str:
        """
        Return the id of the Session.
        """
        return self._session_id

    @property
    def user_id(self) -> str:
        """
        Return the id of the Session's User.
        """
        return self._user_id

    @property
    def start_time(self) -> datetime:
        """
        Return the start date-time of the Session
        """
        return self._start_time

    @property
    def end_time(self) -> datetime:
        """
        Return the end date-time of the Session
        """
        return self._end_time

    def __repr__(self) -> str:

        return 'Session({})'.format(self._session_id)
