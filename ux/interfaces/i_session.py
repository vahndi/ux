from datetime import datetime


class ISession(object):

    @property
    def session_id(self) -> str:

        raise NotImplementedError

    @property
    def user_id(self) -> str:

        raise NotImplementedError

    @property
    def start_time(self) -> datetime:

        raise NotImplementedError

    @property
    def end_time(self) -> datetime:

        raise NotImplementedError
