from ux.interfaces.i_location import ILocation


class Location(ILocation):
    """
    Represents a Location where an Action could be taken.
    """
    def __init__(self, location_id: str):
        """
        Create a new Location.

        :param location_id: The id of the Location.
        """
        self._location_id = location_id

    @property
    def location_id(self):
        """
        Return the id of the Location.

        :rtype: str
        """
        return self._location_id

    def __repr__(self):

        return 'Location({})'.format(self._location_id)

    def __gt__(self, other):
        """
        :type other: Location
        """
        return self._location_id > other._location_id

    def __lt__(self, other):
        """
        :type other: Location
        """
        return self._location_id < other._location_id
