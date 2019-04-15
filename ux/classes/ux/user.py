from ux.interfaces.ux.i_user import IUser


class User(IUser):

    def __init__(self, user_id, session_ids: list = None, action_ids: list = None):

        self._user_id = user_id
        self._session_ids = session_ids or []
        self._action_ids = action_ids or []

    @property
    def user_id(self):
        return self._user_id

    @property
    def action_ids(self):
        return self._action_ids

    @property
    def session_ids(self):
        return self._session_ids

    def add_action_id(self, action_id):

        self._action_ids.append(action_id)

    def add_session_id(self, session_id):

        self._session_ids.append(session_id)

    def __repr__(self):

        return 'User({})'.format(self._user_id)
