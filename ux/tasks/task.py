from typing import List, Iterator, Optional, Tuple

from ux.actions.action_template import ActionTemplate


class Task(object):
    """
    Represents a Task corresponding to a sequence of desirable Actions.
    """
    def __init__(self, name: str, action_templates: List[ActionTemplate] = None):
        """
        Create a new Task.

        :param name: The name of the new Task.
        :param action_templates: A list of ActionTemplates that compose the Task.
        """
        self._name: str = name
        self._action_templates: List[ActionTemplate] = action_templates or []

    @property
    def name(self) -> str:
        """
        Return the name of the Task.
        """
        return self._name

    @property
    def action_templates(self) -> List[ActionTemplate]:
        """
        Return the list of ActionTemplates that compose the Task.
        """
        return self._action_templates

    # region action template property lists

    @property
    def source_ids(self) -> List[str]:
        return [template.source_id for template in self]

    @property
    def target_ids(self) -> List[Optional[str]]:
        return [template.target_id for template in self]

    @property
    def action_types(self) -> List[str]:
        return [template.action_type for template in self]

    @property
    def weightings(self) -> List[float]:
        return [template.weighting for template in self]

    # end region

    def add_action_template(self, action_template: ActionTemplate) -> None:
        """
        Add a new ActionTemplate to the end of the Task.

        :param action_template: The ActionTemplate to add.
        """
        self._action_templates.append(action_template)

    def __len__(self) -> int:

        return len(self._action_templates)

    def __repr__(self) -> str:

        return 'Task({} [{}])'.format(
            self._name, len(self._action_templates)
        )

    def __getitem__(self, item) -> ActionTemplate:

        return self._action_templates[item]

    def __contains__(self, item) -> bool:

        if isinstance(item, ActionTemplate):
            return item in self._action_templates
        else:
            raise TypeError('item must be IActionTemplate')

    def __iter__(self) -> Iterator[ActionTemplate]:

        return self._action_templates.__iter__()


TaskPair = Tuple[Task, Task]