from datetime import timedelta
from matplotlib.axes import Axes
from pandas import concat, DataFrame, MultiIndex, Series, pivot_table
from typing import List
from numpy import nan
from pandas.core.computation.ops import isnumeric
from seaborn import heatmap

from ux.plots.helpers import new_axes, transform_axis_tick_labels, set_axis_tick_label_rotation


class TemporalCount(dict):

    def __init__(self, name: str):
        """
        Create a new Temporal Count representing the count of a single or split variable over time.

        :param name: The name of the metric or measure being counted
        """
        super(TemporalCount, self).__init__()
        self._name = name

    @staticmethod
    def from_dict(dictionary: dict, name: str):
        """
        Create a new Temporal Count from an existing dict.

        :rtype: TemporalCount
        """
        count = TemporalCount(name=name)
        for key, value in dictionary.items():
            count[key] = value
        return count

    @property
    def name(self):
        return self._name

    def rename(self, name: str):
        """
        :rtype: TemporalCount
        """
        self._name = name
        return self

    @property
    def is_split(self):
        """
        :rtype: bool
        """
        values = list(self.values())
        if not values:
            return None
        else:
            return type(values[0]) is dict

    @property
    def frequency(self):
        """
        :rtype: timedelta
        """
        date_times = self.to_frame().index
        return date_times[1] - date_times[0]

    @property
    def freq_str(self):
        """
        :rtype:
        """
        td = self.frequency
        if td.seconds == 3600:
            return 'hourly'
        elif td.seconds == 0:
            if td.days == 1:
                return 'daily'
            elif td.days == 7:
                return 'weekly'
            elif 28 <= td.days <= 31:
                return 'monthly'
            elif 365 <= td.days <= 366:
                return 'annual'
        else:
            return None

    def freq_formatter(self):

        freq_str = self.freq_str
        if freq_str == 'hourly':
            return lambda d: d[-8: -3]
        elif freq_str in ('daily', 'weekly'):
            return lambda d: d[: 10]
        elif freq_str == 'monthly':
            return lambda d: d[: 7]
        elif freq_str == 'annual':
            return lambda d: d[: 4]
        else:
            return lambda d: d

    def to_series(self):
        """
        Return the Series representation of the count data.

        If the count is split, return counts indexed by datetime and count variable.
        If the count is not split return counts indexed by datetime.

        :rtype: Series
        """
        if self.is_split:
            data = DataFrame(self).T
            data.index.name = 'date_time'
            data = data.reset_index().melt(
                id_vars='date_time', var_name=self._name, value_name='count'
            )
            data = data.set_index(['date_time', self._name])['count']
            return data.replace(nan, 0)
        else:
            data = Series(data=self, name=self._name)
            data.index.name = 'date_time'
            return data.replace(nan, 0)

    def to_frame(self):
        """
        Return the DataFrame representation of the count data.

        If the count is split then each split key will be represented by a 2-level column.
        If the count is not split then there will be one column, named after the TemporalCount.
        In either case the Index will be the datetime of the count.

        :rtype: DataFrame
        """
        if self.is_split:
            data = DataFrame(self).T
            data.index.name = 'date_time'
            data.columns = MultiIndex.from_product([[self._name], data.columns])
            return data.replace(nan, 0)
        else:
            return self.to_series().to_frame().replace(nan, 0)

    def to_pandas(self):
        """
        Return the most natural representation of the count as a pandas object.

        :return: Pandas DataFrame if the count is split otherwise a Series
        """
        if self.is_split:
            return self.to_frame()
        else:
            return self.to_series()

    def plot(self, plot_type: str = 'bar', stacked: bool = True, top: int = None,
             ax: Axes = None, axis_kws: dict = None):
        """
        Plot the count.

        :param plot_type: Type of plot for split counts. One of ('bar', 'heatmap')
        :param stacked: If barplot is stacked
        :param top: Number of results to show in heatmaps. Leave as None to show all.
        :param ax: Optional matplotlib axes to plot on
        :param axis_kws: Optional dict of values to call ax.set() with
        :rtype: Axes
        """
        assert(plot_type in ('bar', 'heatmap'))
        ax = ax or new_axes()
        ax.set_title(self.name)
        if self.is_split:
            if plot_type == 'bar':
                data = self.to_frame()
                data.droplevel(0, axis=1).plot.bar(ax=ax, stacked=stacked)
                ax.set_ylabel('Count')
            else:  # heatmap
                data = self.to_series().reset_index()
                pt = pivot_table(data, index='date_time', columns=self.name, values='count').astype(int)
                pt = (
                    pt.append(Series(data=pt.sum(), name='#TOTAL#'))
                      .sort_values('#TOTAL#', axis=1, ascending=False)
                      .drop('#TOTAL#', axis=0)
                )
                if top is not None:
                    pt = pt.T.head(top).T
                heatmap(data=pt.T, annot=True, fmt='d', ax=ax)
                y_lim = ax.get_ylim()
                ax.set_ylim(max(y_lim) + 0.5, min(y_lim) - 0.5)
                set_axis_tick_label_rotation(ax.yaxis, 0)
                ax.set_ylabel(self.name)
        else:
            data = self.to_series()
            data.plot.bar(ax=ax)
        transform_axis_tick_labels(ax.xaxis, self.freq_formatter())
        ax.set_xlabel('Date Time')
        if axis_kws is not None:
            ax.set(**axis_kws)
        return ax

    @staticmethod
    def plot_comparison(temporal_counts, stacked: bool = False,
                        ax: Axes = None, axis_kws: dict = None):
        """
        Plot a comparison of several counts.

        :param temporal_counts: Counts to compare
        :type temporal_counts: List[TemporalCount]
        :param ax: Optional matplotlib axes to plot on
        :param axis_kws: Optional dict of values to call ax.set() with
        """
        data = concat([
            temporal_count.to_series()
            for temporal_count in temporal_counts
        ], axis=1)  # assumes all are not split
        ax = ax or new_axes()
        data.plot.bar(ax=ax, stacked=stacked)
        transform_axis_tick_labels(ax.xaxis, temporal_counts[0].freq_formatter())
        ax.set_xlabel('Date Time')
        ax.set_ylabel('Count')
        if axis_kws is not None:
            ax.set(**axis_kws)
        return ax

    def __truediv__(self, other):
        """
        :rtype: TemporalCount
        """
        if isinstance(other, TemporalCount):
            if self.is_split and not other.is_split:
                raise ValueError("Can't divide a split count by a non-split count.")
            elif not self.is_split and other.is_split:
                raise ValueError("Can't divide a non-split count by a split count.")
            new_name = '{} / {}'.format(self.name, other.name)
            if not self.is_split:
                div_data = (self.to_pandas() / other.to_pandas()).to_dict()
            else:
                div_data = self.to_frame().droplevel(0, axis=1).div(other.to_frame().droplevel(0, axis=1), fill_value=0)
                div_data = div_data.to_dict(orient='index')
            return TemporalCount.from_dict(div_data, name=new_name)
        elif isnumeric(type(other)):
            if self.is_split:
                div_data = (self.to_frame().droplevel(0, axis=1) / other).to_dict(orient='index')
            else:
                div_data = (self.to_series() / other).to_dict()
            return TemporalCount.from_dict(div_data, name='{} / {}'.format(self.name, other))
        else:
            raise TypeError('Can only divide a TemporalCount by another TemporalCount or a numeric value.')

    def __rtruediv__(self, other):
        """
        :rtype: TemporalCount
        """
        if isinstance(other, TemporalCount):
            if self.is_split and not other.is_split:
                raise ValueError("Can't divide a non-split count by a split count.")
            elif not self.is_split and other.is_split:
                raise ValueError("Can't divide a split count by a non-split count.")
            new_name = '{} / {}'.format(other.name, self.name)
            if not self.is_split:
                div_data = (other.to_pandas() / self.to_pandas()).to_dict()
            else:
                div_data = other.to_frame().droplevel(0, axis=1).div(self.to_frame().droplevel(0, axis=1), fill_value=0)
                div_data = div_data.to_dict(orient='index')
            return TemporalCount.from_dict(div_data, name=new_name)
        elif isnumeric(type(other)):
            if self.is_split:
                div_data = (other / self.to_frame().droplevel(0, axis=1)).to_dict(orient='index')
            else:
                div_data = (other / self.to_series()).to_dict()
            return TemporalCount.from_dict(div_data, name='{} / {}'.format(other, self.name))
        else:
            raise TypeError('Can only divide another TemporalCount or a numeric value by a TemporalCount.')

    def __mul__(self, other):
        """
        :rtype: TemporalCount
        """
        if isinstance(other, TemporalCount):
            if self.is_split and not other.is_split:
                raise ValueError("Can't multiply a split count by a non-split count.")
            elif not self.is_split and other.is_split:
                raise ValueError("Can't multiply a non-split count by a split count.")
            new_name = '{} * {}'.format(self.name, other.name)
            if not self.is_split:
                mul_data = (self.to_pandas() * other.to_pandas()).to_dict()
            else:
                mul_data = self.to_frame().droplevel(0, axis=1).mul(other.to_frame().droplevel(0, axis=1), fill_value=0)
                mul_data = mul_data.to_dict(orient='index')
            return TemporalCount.from_dict(mul_data, name=new_name)
        elif isnumeric(type(other)):
            if self.is_split:
                mul_data = (self.to_frame().droplevel(0, axis=1) * other).to_dict(orient='index')
            else:
                mul_data = (self.to_series() * other).to_dict()
            return TemporalCount.from_dict(mul_data, name='{} * {}'.format(self.name, other))
        else:
            raise TypeError('Can only multiply a TemporalCount by another TemporalCount or a numeric value.')

    def __rmul__(self, other):
        """
        :rtype: TemporalCount
        """
        if isinstance(other, TemporalCount):
            if self.is_split and not other.is_split:
                raise ValueError("Can't multiply a split count by a non-split count.")
            elif not self.is_split and other.is_split:
                raise ValueError("Can't multiply a non-split count by a split count.")
            new_name = '{} * {}'.format(other.name, self.name)
            if not self.is_split:
                mul_data = (other.to_pandas() * self.to_pandas()).to_dict()
            else:
                mul_data = other.to_frame().droplevel(0, axis=1).mul(self.to_frame().droplevel(0, axis=1), fill_value=0)
                mul_data = mul_data.to_dict(orient='index')
            return TemporalCount.from_dict(mul_data, name=new_name)
        elif isnumeric(type(other)):
            if self.is_split:
                mul_data = (other * self.to_frame().droplevel(0, axis=1)).to_dict(orient='index')
            else:
                mul_data = (other * self.to_series()).to_dict()
            return TemporalCount.from_dict(mul_data, name='{} * {}'.format(other, self.name))
        else:
            raise TypeError('Can only multiply a TemporalCount by another TemporalCount or a numeric value.')

    def __add__(self, other):
        """
        :rtype: TemporalCount
        """
        if isinstance(other, TemporalCount):
            if self.is_split and not other.is_split:
                raise ValueError("Can't add a split count to a non-split count.")
            elif not self.is_split and other.is_split:
                raise ValueError("Can't add a non-split count to a split count.")
            new_name = '{} + {}'.format(self.name, other.name)
            if not self.is_split:
                add_data = (self.to_pandas() + other.to_pandas()).to_dict()
            else:
                add_data = self.to_frame().droplevel(0, axis=1).add(other.to_frame().droplevel(0, axis=1), fill_value=0)
                add_data = add_data.to_dict(orient='index')
            return TemporalCount.from_dict(add_data, name=new_name)
        elif isnumeric(type(other)):
            if self.is_split:
                add_data = (self.to_frame().droplevel(0, axis=1) + other).to_dict(orient='index')
            else:
                add_data = (self.to_series() + other).to_dict()
            return TemporalCount.from_dict(add_data, name='{} + {}'.format(self.name, other))
        else:
            raise TypeError('Can only add a TemporalCount to another TemporalCount or a numeric value.')

    def __radd__(self, other):
        """
        :rtype: TemporalCount
        """
        if isinstance(other, TemporalCount):
            if self.is_split and not other.is_split:
                raise ValueError("Can't add a split count to a non-split count.")
            elif not self.is_split and other.is_split:
                raise ValueError("Can't add a non-split count to a split count.")
            new_name = '{} + {}'.format(other.name, self.name)
            if not self.is_split:
                add_data = (other.to_pandas() + self.to_pandas()).to_dict()
            else:
                add_data = other.to_frame().droplevel(0, axis=1).add(self.to_frame().droplevel(0, axis=1), fill_value=0)
                add_data = add_data.to_dict(orient='index')
            return TemporalCount.from_dict(add_data, name=new_name)
        elif isnumeric(type(other)):
            if self.is_split:
                add_data = (other + self.to_frame().droplevel(0, axis=1)).to_dict(orient='index')
            else:
                add_data = (other + self.to_series()).to_dict()
            return TemporalCount.from_dict(add_data, name='{} + {}'.format(other, self.name))
        else:
            raise TypeError('Can only add another TemporalCount or a numeric value to a TemporalCount.')

    def __sub__(self, other):
        """
        :rtype: TemporalCount
        """
        if isinstance(other, TemporalCount):
            if self.is_split and not other.is_split:
                raise ValueError("Can't subtract a non-split count from a split count.")
            elif not self.is_split and other.is_split:
                raise ValueError("Can't subtract a split count from a non-split count.")
            new_name = '{} - {}'.format(self.name, other.name)
            if not self.is_split:
                sub_data = (self.to_pandas() - other.to_pandas()).to_dict()
            else:
                sub_data = self.to_frame().droplevel(0, axis=1).sub(other.to_frame().droplevel(0, axis=1), fill_value=0)
                sub_data = sub_data.to_dict(orient='index')
            return TemporalCount.from_dict(sub_data, name=new_name)
        elif isnumeric(type(other)):
            if self.is_split:
                sub_data = (self.to_frame().droplevel(0, axis=1) - other).to_dict(orient='index')
            else:
                sub_data = (self.to_series() - other).to_dict()
            return TemporalCount.from_dict(sub_data, name='{} - {}'.format(self.name, other))
        else:
            raise TypeError(
                'Can only subtract another TemporalCount or a numeric value from a TemporalCount.'
            )

    def __rsub__(self, other):
        """
        :rtype: TemporalCount
        """
        if isinstance(other, TemporalCount):
            if self.is_split and not other.is_split:
                raise ValueError("Can't subtract a split count from a non-split count.")
            elif not self.is_split and other.is_split:
                raise ValueError("Can't subtract a non-split count from a split count.")
            new_name = '{} - {}'.format(other.name, self.name)
            if not self.is_split:
                sub_data = (other.to_pandas() - self.to_pandas()).to_dict()
            else:
                sub_data = other.to_frame().droplevel(0, axis=1).sub(self.to_frame().droplevel(0, axis=1), fill_value=0)
                sub_data = sub_data.to_dict(orient='index')
            return TemporalCount.from_dict(sub_data, name=new_name)
        elif isnumeric(type(other)):
            if self.is_split:
                sub_data = (other - self.to_frame().droplevel(0, axis=1)).to_dict(orient='index')
            else:
                sub_data = (other - self.to_series()).to_dict()
            return TemporalCount.from_dict(sub_data, name='{} - {}'.format(other, self.name))
        else:
            raise TypeError(
                'Can only subtract a TemporalCount from another TemporalCount or a numeric value.'
            )
