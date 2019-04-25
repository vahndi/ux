from typing import List


class IDatabaseManager(object):
    """
    An interface or abstract base class that should be implemented for each new backend.
    """
    def session(self, session_id: str):
        """
        Return the Session with the given id.

        :rtype: ISession
        """
        raise NotImplementedError

    def sessions(self):
        """
        Return all the Sessions in the database.

        :rtype: List[ISession]
        """
        raise NotImplementedError

    def user(self, user_id: str):
        """
        :rtype: IUser
        """
        raise NotImplementedError

    def users(self):
        """
        Return all the Users in the database.

        :rtype: List[IUser]
        """
        raise NotImplementedError

    def user_action(self, action_id: str):
        """
        Return the UserAction with the given id.

        :rtype: IUserAction
        """
        raise NotImplementedError

    def user_actions(self, user_id: str):
        """
        Return all the Actions taken by the User with the given id in the database.

        :rtype: List[IUserAction]
        """
        raise NotImplementedError

    def location(self, location_id: str):
        """
        Return the Location with the given id.

        :rtype: ILocation
        """
        raise NotImplementedError

    def locations(self):
        """
        Return all the Locations in the database.

        :rtype: List[ILocation]
        """
        raise NotImplementedError

    def action_types(self):
        """
        Return all the Action Types embedded in UserActions.

        :rtype: List[str]
        """
        raise NotImplementedError

    def get_session_sequence(self, session_id):
        """
        Return an ActionSequence constructed from all UserActions in the Session with the given id.

        :rtype: IActionSequence
        """
        raise NotImplementedError
