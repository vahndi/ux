from collections import OrderedDict
from pandas import DataFrame, Series, MultiIndex, Index, concat
from typing import Iterable, Iterator, List, Union, ItemsView, KeysView, ValuesView


def _str_or_non_iterable(val) -> bool:

    return not isinstance(val, Iterable) or isinstance(val, str)


class MapResult(object):

    def __init__(self, data: dict,
                 key_names: Union[str, List[str]] = 'map',
                 value_names: Union[str, List[str]] = 'result'):

        if isinstance(key_names, str):
            key_names = [key_names]
        if isinstance(value_names, str):
            value_names = [value_names]

        # check key names
        if all(_str_or_non_iterable(k) for k in list(data.keys())):
            if not len(key_names) == 1:
                raise ValueError(
                    'Length of index names must be '
                    '1 when keys are not Iterables'
                )
        else:
            if not len(key_names) == len(list(data.keys())[0]):
                raise KeyError(
                    'Keys must have same length as key_names'
                )

        # check value names
        if not len(value_names) == 1:
            raise ValueError('value_names must be length 1')

        self._data: dict = data
        self._key_names: List[str] = key_names
        self._value_names: List[str] = value_names

        self._first_key = list(data.keys())[0]
        self._first_value = list(data.values())[0]

        for attribute in self._data.keys():
            try:
                setattr(self, attribute, self._data[attribute])
            except:
                pass

    @property
    def key_names(self) -> List[str]:

        return self._key_names

    @property
    def value_names(self) -> List[str]:

        return self._value_names

    def to_series(self) -> Series:

        if _str_or_non_iterable(self._first_key):
            if _str_or_non_iterable(self._first_value):
                # e.g. {'a': 1, 'b': 2, 'c': 3}
                series = Series(self._data, name=self.value_names[0])
                series.index.name = self.key_names[0]
            else:
                # e.g. {'a': [1, 2], 'b': [3, 4, 5]}
                series = concat([
                    Series(
                        index=Index([key] * len(values),
                                    name=self.key_names[0]),
                        data=values, name=self.value_names[0]
                    )
                    for key, values in self._data.items()
                ])
        else:
            if _str_or_non_iterable(self._first_value):
                # e.g. {('a', 'b'): 1, ('c', 'd'): 2, ('e', 'f'): 3}
                series = Series(self._data, name=self.value_names[0])
                series.index.names = self.key_names
            else:
                # e.g. {('a', 'b'): [1, 2], ('c', 'd'): [3, 4, 5]}
                series = concat([
                    Series(
                        index=MultiIndex.from_tuples(tuples=[key] * len(values),
                                                     names=self.key_names),
                        data=values, name=self.value_names[0]
                    )
                    for key, values in self._data.items()
                ])

        return series

    def to_dict(self) -> dict:

        return self._data

    def to_frame(self, wide: bool = False) -> DataFrame:

        if not wide:
            return self.to_series().to_frame().reset_index()
        else:
            try:
                return DataFrame(self._data)
            except:
                return self.to_series().to_frame().reset_index()

    def to_list(self) -> list:

        return list(self.to_series().tolist())

    def to_tuples(self) -> List[tuple]:

        return list(self.to_frame().to_records())

    def items(self) -> ItemsView:

        return self._data.items()

    def keys(self) -> KeysView:

        return self._data.keys()

    def values(self) -> ValuesView:

        return self._data.values()

    def __getitem__(self, item):

        return self._data[item]

    def __iter__(self) -> Iterator[dict]:

        return self._data.__iter__()

    def __repr__(self) -> str:

        return 'MapResult({})'.format(self._data.__repr__())

    def __eq__(self, other: 'MapResult') -> bool:

        return (
            self.key_names == other.key_names and
            self.value_names == other.value_names and
            self._data == other._data
        )

    def __add__(self, other: 'MapResult') -> 'MapResult':
        """
        Add the values of this MapResult to the values of the other by key.

        If key does not exist in one of the MapResults, uses the value from the
        one where it does.
        """
        if self.key_names != other.key_names:
            raise KeyError('Key names must be identical')
        if self.value_names != other.value_names:
            raise ValueError('Value names must be identical')
        new_data = OrderedDict()
        for key in self.keys():
            if key in other.keys():
                new_data[key] = self[key] + other[key]
            else:
                new_data[key] = self[key]
        for key in other.keys():
            if key not in self.keys():
                new_data[key] = other[key]
        return MapResult(
            data=new_data,
            key_names=self.key_names,
            value_names=self.value_names
        )

    def __sub__(self, other: 'MapResult') -> 'MapResult':
        """
        Subtract the values of the other MapResult from the values of this one
        by key.

        If key does not exist in this MapResult tries to negate the value of the
        other.
        If key does not exist in the other MapResult uses the value of this one.
        """
        if self.key_names != other.key_names:
            raise KeyError('Key names must be identical')
        if self.value_names != other.value_names:
            raise ValueError('Value names must be identical')
        new_data = OrderedDict()
        for key in self.keys():
            if key in other.keys():
                new_data[key] = self[key] - other[key]
            else:
                new_data[key] = self[key]
        for key in other.keys():
            if key not in self.keys():
                new_data[key] = -other[key]
        return MapResult(
            data=new_data,
            key_names=self.key_names,
            value_names=self.value_names
        )

    def __mul__(self, other: 'MapResult') -> 'MapResult':
        """
        Multiply the values of this MapResult to the values of the other by key.

        If key does not exist in one of the MapResults, omits the key from the
        new result.
        """
        if self.key_names != other.key_names:
            raise KeyError('Key names must be identical')
        if self.value_names != other.value_names:
            raise ValueError('Value names must be identical')
        new_data = OrderedDict()
        for key in self.keys():
            if key in other.keys():
                if (
                        not isinstance(self[key], Iterable) and
                        not isinstance(other[key], Iterable)
                ):
                    new_data[key] = self[key] * other[key]
                else:
                    raise TypeError(
                        'Cannot multiple iterable value by non-iterable value'
                    )
        return MapResult(
            data=new_data,
            key_names=self.key_names,
            value_names=self.value_names
        )

    def __truediv__(self, other: 'MapResult') -> 'MapResult':
        """
        Divide the values of this MapResult to the values of the other by key.

        If key does not exist in one of the MapResults, omits the key from the
        new result.
        """
        if self.key_names != other.key_names:
            raise KeyError('Key names must be identical')
        if self.value_names != other.value_names:
            raise ValueError('Value names must be identical')
        new_data = OrderedDict()
        for key in self.keys():
            if key in other.keys():
                new_data[key] = self[key] / other[key]
        return MapResult(
            data=new_data,
            key_names=self.key_names,
            value_names=self.value_names
        )
