from collections import defaultdict

from ux.interfaces.actions.i_action_sequence import IActionSequence
from ux.interfaces.i_database_manager import IDatabaseManager


def find_location_history(manager: IDatabaseManager):
    """
    Find the history of each Location's appearance in the Database.

    :param manager: Instance of a class inheriting from IDatabaseManager.
    :return: Dictionary mapping location ids to lists of session start times.
    :rtype: dict
    """
    history = defaultdict(list)
    for session in manager.sessions():
        session_start = session.start_time
        sequence: IActionSequence = manager.get_session_sequence(session_id=session.session_id)
        for location_id in sequence.location_ids():
            history[location_id].append(session_start)
    return dict(history)
