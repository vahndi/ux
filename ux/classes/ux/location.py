from ux.interfaces.ux.i_location import ILocation


class Location(ILocation):

    def __init__(self, location_id: str):

        self._location_id = location_id

    @property
    def location_id(self):
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
