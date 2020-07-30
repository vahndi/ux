from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from ux.sequences.action_sequence import ActionSequence
from ux.database_manager import DatabaseManager


def find_location_history(
        manager: DatabaseManager,
        start: datetime = None,
        end: datetime = None
) -> Dict[str, List[datetime]]:
    """
    Find the history of each Location's appearance in the Database.

    :param manager: Instance of a class inheriting from IDatabaseManager.
    :param start: Optional start date-time to exclude older sessions.
    :param end: Optional end date-time to exclude newer sessions.
    :return: Dictionary mapping location ids to lists of session start times.
    """
    history = defaultdict(list)
    for session in manager.sessions():
        session_start = session.start_time
        if (start and session_start < start) or (end and (session_start > end)):
            continue
        sequence: ActionSequence = manager.get_session_sequence(
            session_id=session.session_id
        )
        for location_id in sequence.location_ids():
            history[location_id].append(session_start)
    return dict(history)


def find_action_type_history(
        manager: DatabaseManager,
        start: datetime = None,
        end: datetime = None
) -> Dict[str, List[datetime]]:
    """
    Find the history of each Action Type's appearance in the Database.

    :param manager: Instance of a class inheriting from IDatabaseManager.
    :param start: Optional start date-time to exclude older sessions.
    :param end: Optional end date-time to exclude newer sessions.
    :return: Dictionary mapping location ids to lists of session start times.
    """
    history = defaultdict(list)
    for session in manager.sessions():
        session_start = session.start_time
        if (start and session_start < start) or (end and (session_start > end)):
            continue
        sequence: ActionSequence = manager.get_session_sequence(
            session_id=session.session_id
        )
        for action_type in sequence.unique_action_types():
            history[action_type].append(session_start)
    return dict(history)
