from typing import List


class IUser(object):

    @property
    def user_id(self) -> str:

        raise NotImplementedError

    @property
    def session_ids(self) -> List[str]:

        raise NotImplementedError

    @property
    def action_ids(self) -> List[str]:

        raise NotImplementedError

    def add_action_id(self, action_id):
        raise NotImplementedError

    def add_session_id(self, session_id):
        raise NotImplementedError
