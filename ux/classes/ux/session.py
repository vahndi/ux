from ux.interfaces.ux.i_session import ISession


class Session(ISession):

    def __init__(self, session_id, user_id, start_time, end_time):

        self._session_id = session_id
        self._user_id = user_id or None
        self._start_time = start_time
        self._end_time = end_time

    @property
    def session_id(self):
        return self._session_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    def __repr__(self):

        return 'Session({})'.format(self._session_id)
