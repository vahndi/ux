class ISession(object):

    @property
    def session_id(self):
        raise NotImplementedError

    @property
    def user_id(self):
        raise NotImplementedError

    @property
    def start_time(self):
        raise NotImplementedError

    @property
    def end_time(self):
        raise NotImplementedError
