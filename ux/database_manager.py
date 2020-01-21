from abc import ABC
from typing import List

from ux.classes.sequences.action_sequence import ActionSequence
from ux.classes.location import Location
from ux.classes.session import Session
from ux.classes.user import User
from ux.classes.actions.user_action import UserAction


class DatabaseManager(ABC):
    """
    An abstract base class that should be implemented for each new backend.
    """
    def session(self, session_id: str) -> Session:
        """
        Return the Session with the given id.
        """
        raise NotImplementedError

    def sessions(self) -> List[Session]:
        """
        Return all the Sessions in the database.
        """
        raise NotImplementedError

    def user(self, user_id: str) -> User:

        raise NotImplementedError

    def users(self) -> List[User]:
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

    def location(self, location_id: str) -> Location:
        """
        Return the Location with the given id.
        """
        raise NotImplementedError

    def locations(self) -> List[Location]:
        """
        Return all the Locations in the database.
        """
        raise NotImplementedError

    def action_types(self) -> List[str]:
        """
        Return all the Action Types embedded in UserActions.
        """
        raise NotImplementedError

    def get_session_sequence(self, session_id) -> ActionSequence:
        """
        Return an ActionSequence constructed from all UserActions in the Session with the given id.
        """
        raise NotImplementedError
