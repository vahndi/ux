from typing import List

from ux.classes.ux.session import Session


class IDatabaseManager(object):

    def session(self, session_id: str):
        """
        :rtype: Session
        """
        raise NotImplementedError

    def sessions(self):
        """
        :rtype: List[Session]
        """
        raise NotImplementedError

    def user(self, user_id: str):
        """
        :rtype: User
        """
        raise NotImplementedError

    def users(self):
        """
        :rtype: List[User]
        """
        raise NotImplementedError

    def user_action(self, action_id: str):
        """
        :rtype: UserAction
        """
        raise NotImplementedError

    def user_actions(self, user_id: str):
        """
        :rtype: List[UserAction]
        """
        raise NotImplementedError

    def location(self, location_id: str):
        """
        :rtype: Location
        """
        raise NotImplementedError

    def locations(self):
        """
        :rtype: List[Location]
        """
        raise NotImplementedError

    def get_session_sequence(self, session_id):
        """
        :rtype: IActionSequence
        """
        raise NotImplementedError
