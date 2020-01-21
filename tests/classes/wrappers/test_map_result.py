from itertools import product
from typing import List
from unittest import TestCase

from pandas import Series, Index, DataFrame

from ux.wrappers.map_result import MapResult


class TestMapResult(TestCase):

    def setUp(self) -> None:

        self.mr_single_single: MapResult = MapResult(
            data={'a': 1, 'b': 2, 'c': 3},
            key_names='letters',
            value_names='numbers'
        )
        self.s_single_single: Series = Series(
            index=Index(data=['a', 'b', 'c'], name='letters'),
            data=[1, 2, 3], name='numbers'
        )
        self.mr_single_fixed: MapResult = MapResult(
            data={'a': [1, 2, 3], 'b': [4, 5, 6]},
            key_names='letters',
            value_names='numbers'
        )
        self.s_single_fixed: Series = Series(
            index=Index(data=['a', 'a', 'a', 'b', 'b', 'b'], name='letters'),
            data=[1, 2, 3, 4, 5, 6], name='numbers'
        )
        self.d_data_fixed_wide: DataFrame = DataFrame(
            data={'a': [1, 2, 3], 'b': [4, 5, 6]}
        )
        self.mr_single_variable: MapResult = MapResult(
            data={'a': [1, 2], 'b': [3, 4, 5]},
            key_names='letters',
            value_names='numbers'
        )
        self.s_single_variable: Series = Series(
            index=Index(data=['a', 'a', 'b', 'b', 'b'], name='letters'),
            data=[1, 2, 3, 4, 5], name='numbers'
        )
        self.mr_tuple_single: MapResult = MapResult(
            data={('a', 'b'): 1, ('c', 'd'): 2, ('e', 'f'): 3},
            key_names=['letter_1', 'letter_2'],
            value_names='numbers'
        )
        self.s_tuple_single: Series = Series(
            index=Index(data=[('a', 'b'), ('c', 'd'), ('e', 'f')], names=['letter_1', 'letter_2']),
            data=[1, 2, 3], name='numbers'
        )
        self.mr_tuple_fixed: MapResult = MapResult(
            data={('a', 'b'): [1, 2, 3], ('c', 'd'): [4, 5, 6]},
            key_names=['letter_1', 'letter_2'],
            value_names='numbers'
        )
        self.s_tuple_fixed: Series = Series(
            index=Index(data=[('a', 'b'), ('a', 'b'), ('a', 'b'), ('c', 'd'), ('c', 'd'), ('c', 'd')],
                        names=['letter_1', 'letter_2']),
            data=[1, 2, 3, 4, 5, 6], name='numbers'
        )
        self.mr_tuple_variable: MapResult = MapResult(
            data={('a', 'b'): [1, 2], ('c', 'd'): [3, 4, 5]},
            key_names=['letter_1', 'letter_2'],
            value_names='numbers'
        )
        self.s_tuple_variable: Series = Series(
            index=Index(data=[('a', 'b'), ('a', 'b'), ('c', 'd'), ('c', 'd'), ('c', 'd')],
                        names=['letter_1', 'letter_2']),
            data=[1, 2, 3, 4, 5], name='numbers'
        )
        self.mr_single_key: List[MapResult] = [
            self.mr_single_single, self.mr_single_fixed, self.mr_single_variable
        ]
        self.mr_tuple_key: List[MapResult] = [
            self.mr_tuple_single, self.mr_tuple_fixed, self.mr_tuple_variable
        ]

    @staticmethod
    def series_equivalent(data_1: Series, data_2: Series) -> bool:

        return (
            data_1.index.tolist() == data_2.index.tolist() and
            data_1.to_list() == data_2.to_list()
        )

    @staticmethod
    def frames_equivalent(data_1: DataFrame, data_2: DataFrame) -> bool:

        return (
            sorted(data_1.columns) == sorted(data_2.columns) and
            data_1.index.to_list() == data_2.index.to_list()
            and all(data_1[column].to_list() == data_2[column].to_list() for column in data_1.columns)
        )

    def test_to_series(self):

        self.assertTrue(self.series_equivalent(self.s_single_single, self.mr_single_single.to_series()))
        self.assertTrue(self.series_equivalent(self.s_single_fixed, self.mr_single_fixed.to_series()))
        self.assertTrue(self.series_equivalent(self.s_single_variable, self.mr_single_variable.to_series()))
        self.assertTrue(self.series_equivalent(self.s_tuple_single, self.mr_tuple_single.to_series()))
        self.assertTrue(self.series_equivalent(self.s_tuple_fixed, self.mr_tuple_fixed.to_series()))
        self.assertTrue(self.series_equivalent(self.s_tuple_variable, self.mr_tuple_variable.to_series()))

    def test_to_frame(self):

        self.assertTrue(
            self.frames_equivalent(self.s_single_single.reset_index(), self.mr_single_single.to_frame())
        )
        self.assertTrue(
            self.frames_equivalent(self.s_single_fixed.reset_index(), self.mr_single_fixed.to_frame())
        )
        self.assertTrue(
            self.frames_equivalent(self.s_single_variable.reset_index(), self.mr_single_variable.to_frame())
        )
        self.assertTrue(
            self.frames_equivalent(self.s_tuple_single.reset_index(), self.mr_tuple_single.to_frame())
        )
        self.assertTrue(
            self.frames_equivalent(self.s_tuple_fixed.reset_index(), self.mr_tuple_fixed.to_frame())
        )
        self.assertTrue(
            self.frames_equivalent(self.s_tuple_variable.reset_index(), self.mr_tuple_variable.to_frame())
        )

    def test_to_frame_wide(self):

        self.assertTrue(self.frames_equivalent(self.d_data_fixed_wide, self.mr_single_fixed.to_frame(wide=True)))

    def test_add_works(self):

        self.assertEqual(
            self.mr_single_single + self.mr_single_single,
            MapResult(
                data={'a': 2, 'b': 4, 'c': 6},
                key_names='letters', value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_single_fixed + self.mr_single_fixed,
            MapResult(
                data={'a': [1, 2, 3, 1, 2, 3], 'b': [4, 5, 6, 4, 5, 6]},
                key_names='letters', value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_single_variable + self.mr_single_variable,
            MapResult(
                data={'a': [1, 2, 1, 2], 'b': [3, 4, 5, 3, 4, 5]},
                key_names='letters', value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_tuple_single + self.mr_tuple_single,
            MapResult(
                data={('a', 'b'): 2, ('c', 'd'): 4, ('e', 'f'): 6},
                key_names=['letter_1', 'letter_2'], value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_tuple_fixed + self.mr_tuple_fixed,
            MapResult(
                data={('a', 'b'): [1, 2, 3, 1, 2, 3], ('c', 'd'): [4, 5, 6, 4, 5, 6]},
                key_names=['letter_1', 'letter_2'], value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_tuple_variable + self.mr_tuple_variable,
            MapResult(
                data={('a', 'b'): [1, 2, 1, 2], ('c', 'd'): [3, 4, 5, 3, 4, 5]},
                key_names=['letter_1', 'letter_2'], value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_single_fixed + self.mr_single_variable,
            MapResult(
                data={'a': [1, 2, 3, 1, 2], 'b': [4, 5, 6, 3, 4, 5]},
                key_names=['letters'], value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_tuple_fixed + self.mr_tuple_variable,
            MapResult(
                data={('a', 'b'): [1, 2, 3, 1, 2], ('c', 'd'): [4, 5, 6, 3, 4, 5]},
                key_names=['letter_1', 'letter_2'], value_names='numbers'
            )
        )

    def test_add_fails(self):

        # mismatching key types
        for mr_1, mr_2 in product(
            self.mr_single_key, self.mr_tuple_key
        ):
            self.assertRaises(KeyError, lambda: mr_1 + mr_2)
        # unaddable value types
        for mr_1, mr_2 in [
            (self.mr_single_single, self.mr_single_fixed),
            (self.mr_single_single, self.mr_single_variable),
            (self.mr_tuple_single, self.mr_tuple_fixed),
            (self.mr_tuple_single, self.mr_tuple_variable),
        ]:
            self.assertRaises(TypeError, lambda: mr_1 + mr_2)

    def test_sub_works(self):

        self.assertEqual(
            self.mr_single_single - self.mr_single_single,
            MapResult(
                data={'a': 0, 'b': 0, 'c': 0},
                key_names='letters', value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_tuple_single - self.mr_tuple_single,
            MapResult(
                data={('a', 'b'): 0, ('c', 'd'): 0, ('e', 'f'): 0},
                key_names=['letter_1', 'letter_2'], value_names='numbers'
            )
        )

    def test_sub_fails(self):

        # mismatching key types
        for mr_1, mr_2 in product(
            self.mr_single_key, self.mr_tuple_key
        ):
            self.assertRaises(KeyError, lambda: mr_1 - mr_2)
        # unsubtractable value types
        for mr_1, mr_2 in [
            (self.mr_single_single, self.mr_single_fixed),
            (self.mr_single_single, self.mr_single_variable),
            (self.mr_single_fixed, self.mr_single_variable),
            (self.mr_tuple_single, self.mr_tuple_fixed),
            (self.mr_tuple_single, self.mr_tuple_variable),
            (self.mr_tuple_fixed, self.mr_tuple_variable)
        ]:
            self.assertRaises(TypeError, lambda: mr_1 - mr_2)

    def test_mul_works(self):

        self.assertEqual(
            self.mr_single_single * self.mr_single_single,
            MapResult(
                data={'a': 1, 'b': 4, 'c': 9},
                key_names='letters', value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_tuple_single * self.mr_tuple_single,
            MapResult(
                data={('a', 'b'): 1, ('c', 'd'): 4, ('e', 'f'): 9},
                key_names=['letter_1', 'letter_2'], value_names='numbers'
            )
        )

    def test_mul_fails(self):

        # mismatching key types
        for mr_1, mr_2 in product(
            self.mr_single_key, self.mr_tuple_key
        ):
            self.assertRaises(KeyError, lambda: mr_1 * mr_2)
        # unmultipliable value types
        for mr_1, mr_2 in [
            (self.mr_single_single, self.mr_single_fixed),
            (self.mr_single_single, self.mr_single_variable),
            (self.mr_single_fixed, self.mr_single_variable),
            (self.mr_tuple_single, self.mr_tuple_fixed),
            (self.mr_tuple_single, self.mr_tuple_variable),
            (self.mr_tuple_fixed, self.mr_tuple_variable)
        ]:
            self.assertRaises(TypeError, lambda: mr_1 * mr_2)

    def test_div_works(self):

        self.assertEqual(
            self.mr_single_single / self.mr_single_single,
            MapResult(
                data={'a': 1, 'b': 1, 'c': 1},
                key_names='letters', value_names='numbers'
            )
        )
        self.assertEqual(
            self.mr_tuple_single / self.mr_tuple_single,
            MapResult(
                data={('a', 'b'): 1, ('c', 'd'): 1, ('e', 'f'): 1},
                key_names=['letter_1', 'letter_2'], value_names='numbers'
            )
        )

    def test_div_fails(self):

        # mismatching key types
        for mr_1, mr_2 in product(
            self.mr_single_key, self.mr_tuple_key
        ):
            self.assertRaises(KeyError, lambda: mr_1 / mr_2)
        # indivisible value types
        for mr_1, mr_2 in [
            (self.mr_single_single, self.mr_single_fixed),
            (self.mr_single_single, self.mr_single_variable),
            (self.mr_single_fixed, self.mr_single_variable),
            (self.mr_tuple_single, self.mr_tuple_fixed),
            (self.mr_tuple_single, self.mr_tuple_variable),
            (self.mr_tuple_fixed, self.mr_tuple_variable)
        ]:
            self.assertRaises(TypeError, lambda: mr_1 / mr_2)
