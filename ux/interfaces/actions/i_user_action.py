from datetime import datetime

from ux.interfaces.actions.i_action_template import IActionTemplate


class IUserAction(object):

    @property
    def action_type(self) -> str:

        raise NotImplementedError

    @property
    def source_id(self) -> str:

        raise NotImplementedError

    @property
    def target_id(self) -> str:

        raise NotImplementedError

    @property
    def action_id(self) -> str:

        raise NotImplementedError

    @property
    def time_stamp(self) -> datetime:

        raise NotImplementedError

    @property
    def user_id(self) -> str:

        raise NotImplementedError

    @property
    def session_id(self) -> str:

        raise NotImplementedError

    @property
    def meta(self) -> dict:

        raise NotImplementedError

    def template(self) -> IActionTemplate:

        raise NotImplementedError
