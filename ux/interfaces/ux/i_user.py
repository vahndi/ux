class IUser(object):

    @property
    def user_id(self):
        raise NotImplementedError

    @property
    def session_ids(self):
        raise NotImplementedError

    @property
    def action_ids(self):
        raise NotImplementedError

    def add_action_id(self, action_id):
        raise NotImplementedError

    def add_session_id(self, session_id):
        raise NotImplementedError
