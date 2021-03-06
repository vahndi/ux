from math import cos, sin, radians
from types import FunctionType

import matplotlib.pyplot as plt
from matplotlib.axis import Axis
from matplotlib.axes import Axes
from typing import List, Union

from ux.location import Location
from ux.compound_types import FloatPair


def new_axes(width: int = 16, height: int = 9) -> Axes:

    _, ax = plt.subplots(figsize=(width, height))
    return ax


def set_axis_tick_label_rotation(ax: Axis, rotation: int) -> None:
    """
    Set the rotation of axis tick labels.

    :param ax: The axis whose tick label rotation to set.
    :param rotation: The rotation value to set.
    """
    if ax.get_majorticklabels():
        plt.setp(ax.get_majorticklabels(), rotation=rotation)
    if ax.get_minorticklabels():
        plt.setp(ax.get_minorticklabels(), rotation=rotation)


def get_hist_index(bin_values: List[int]) -> List[str]:
    """
    Return index labels for histogram bin values.
    """
    return [
        '{}%-{}%'.format(bin_values[b], bin_values[b + 1])
        for b in range(len(bin_values) - 1)
    ]


def point_distance(point_1: tuple, point_2: tuple) -> float:
    """
    Calculate the distance from point_1 to point_2.
    """
    return (
        (point_1[0] - point_2[0]) ** 2 +
        (point_1[1] - point_2[1]) ** 2
    ) ** 0.5


def circle_edge(point_1: tuple, point_2: tuple, radius: float, rotation_angle: float = 0.0) -> FloatPair:
    """
    Calculate the closest point on the edge of a circle centered at point_1 with radius to point_2.
    """
    distance = point_distance(point_1, point_2)
    edge_point = (
        point_1[0] + radius * (point_2[0] - point_1[0]) / distance,
        point_1[1] + radius * (point_2[1] - point_1[1]) / distance
    )
    if rotation_angle != 0:
        rotation_angle = radians(rotation_angle)
        ox, oy = point_1
        px, py = edge_point
        qx = ox + cos(rotation_angle) * (px - ox) - sin(rotation_angle) * (py - oy)
        qy = oy + sin(rotation_angle) * (px - ox) + cos(rotation_angle) * (py - oy)
        edge_point = qx, qy

    return edge_point


def get_color(color: Union[None, str, FunctionType], state: Location, default: str) -> str:
    """
    Return a matplotlib color string depending on the type of `color`

    :param color: `string` to pass through, `None` to use default or `callable` to use a function.
    :param state: The location to use if `color` is a `callable`.
    :param default: Default color value if `None` was passed.
    """
    if color is None:
        return default
    elif type(color) is str:
        return color
    elif callable(color):
        return color(state)
    else:
        raise TypeError


def transform_axis_tick_labels(ax: Axis, transformation: FunctionType) -> None:
    """
    Transforms the labels of each label along the axis by a transformation function.

    :param ax: The axis whose tick labels to transform.
    :param transformation: The transformation function e.g. `lambda t: t.split('T')[0]`.
    """
    ax.figure.canvas.draw()  # make sure the figure has been drawn so the labels are available to be got
    labels = ax.get_ticklabels()
    for label in labels:
        new_label = transformation(label.get_text())
        label.set_text(new_label)
    ax.set_ticklabels(labels)
