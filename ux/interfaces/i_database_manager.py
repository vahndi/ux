from typing import List

from ux.classes.actions.user_action import UserAction
from ux.interfaces.i_location import ILocation
from ux.interfaces.i_session import ISession
from ux.interfaces.i_user import IUser
from ux.interfaces.sequences.i_action_sequence import IActionSequence


class IDatabaseManager(object):
    """
    An interface or abstract base class that should be implemented for each new backend.
    """
    def session(self, session_id: str) -> ISession:
        """
        Return the Session with the given id.
        """
        raise NotImplementedError

    def sessions(self) -> List[ISession]:
        """
        Return all the Sessions in the database.
        """
        raise NotImplementedError

    def user(self, user_id: str) -> IUser:

        raise NotImplementedError

    def users(self) -> List[IUser]:
        """
        Return all the Users in the database.
        """
        raise NotImplementedError

    def user_action(self, action_id: str) -> UserAction:
        """
        Return the UserAction with the given id.
        """
        raise NotImplementedError

    def user_actions(self, user_id: str) -> List[UserAction]:
        """
        Return all the Actions taken by the User with the given id in the database.
        """
        raise NotImplementedError

    def location(self, location_id: str) -> ILocation:
        """
        Return the Location with the given id.
        """
        raise NotImplementedError

    def locations(self) -> List[ILocation]:
        """
        Return all the Locations in the database.
        """
        raise NotImplementedError

    def action_types(self) -> List[str]:
        """
        Return all the Action Types embedded in UserActions.
        """
        raise NotImplementedError

    def get_session_sequence(self, session_id) -> IActionSequence:
        """
        Return an ActionSequence constructed from all UserActions in the Session with the given id.
        """
        raise NotImplementedError
