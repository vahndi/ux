from typing import List


class ActionTypeFactory(object):

    @staticmethod
    def page_view(sources: List[str], **kwargs) -> List[str]:
        """
        Return every action as a "page-view" action type.

        :param sources: List of source locations,
        """
        return ['page-view'] * len(sources)

    @staticmethod
    def page_view__back_click(sources: List[str], targets: List[str], **kwargs) -> List[str]:
        """
        Return forward actions as "page-view"s and backwards actions as "back-click" action type.

        :param sources: List of source locations.
        :param targets: List of target locations.
        """
        action_types = []
        for source, target in zip(sources, targets):
            if target > source:
                action_types.append('page-view')
            elif source > target:
                action_types.append('back-click')
            else:
                raise ValueError('source cannot equal target')
        return action_types
