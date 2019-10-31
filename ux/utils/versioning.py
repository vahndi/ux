from collections import defaultdict
from datetime import datetime

from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.interfaces.i_database_manager import IDatabaseManager


def find_location_history(manager: IDatabaseManager, start: datetime = None, end: datetime = None):
    """
    Find the history of each Location's appearance in the Database.

    :param manager: Instance of a class inheriting from IDatabaseManager.
    :param start: Optional start date-time to exclude older sessions.
    :param end: Optional end date-time to exclude newer sessions.
    :return: Dictionary mapping location ids to lists of session start times.
    :rtype: dict
    """
    history = defaultdict(list)
    for session in manager.sessions():
        session_start = session.start_time
        if (start and session_start < start) or (end and (session_start > end)):
            continue
        sequence: IActionSequence = manager.get_session_sequence(session_id=session.session_id)
        for location_id in sequence.location_ids():
            history[location_id].append(session_start)
    return dict(history)


def find_action_type_history(manager: IDatabaseManager, start: datetime = None, end: datetime = None):
    """
    Find the history of each Action Type's appearance in the Database.

    :param manager: Instance of a class inheriting from IDatabaseManager.
    :param start: Optional start date-time to exclude older sessions.
    :param end: Optional end date-time to exclude newer sessions.
    :return: Dictionary mapping location ids to lists of session start times.
    :rtype: dict
    """
    history = defaultdict(list)
    for session in manager.sessions():
        session_start = session.start_time
        if (start and session_start < start) or (end and (session_start > end)):
            continue
        sequence: IActionSequence = manager.get_session_sequence(session_id=session.session_id)
        for action_type in sequence.action_types():
            history[action_type].append(session_start)
    return dict(history)
