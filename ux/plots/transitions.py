from datetime import timedelta
from matplotlib.axes import Axes
from matplotlib.dates import DateFormatter, MinuteLocator, HourLocator, DayLocator, SecondLocator, MonthLocator, \
    YearLocator
from matplotlib.patches import Circle, FancyArrowPatch, ConnectionStyle, ArrowStyle
from numpy.ma import arange
from pandas import notnull
from seaborn import heatmap
from typing import Dict, List

from ux.interfaces.sequences.i_action_sequence import IActionSequence
from ux.plots.helpers import new_axes, point_distance, circle_edge, get_color
from ux.utils.transitions import create_transition_matrix


def plot_transition_matrix(transitions, get_name=None,
                           order_by='from', exclude=None,
                           ax: Axes = None, heatmap_kws: dict = None) -> Axes:
    """
    Plot a state transition matrix from the given transition counts or probabilities.

    :param transitions: Dictionary of transitions and their counts or probabilities.
    :type transitions: Dict[Tuple[object, object], Union[float, int]]
    :param get_name: Optional lambda function to call to convert states to labels.
    :type get_name: Callable[[IUserAction], str]
    :param order_by: Order labels by descending count of `from` or `to`, or pass a list to set order explicitly.
    :type order_by: Union[str, List[str]]
    :param exclude: Optional list of labels to exclude from the plots.
    :type exclude: Union[str, List[str]]
    :param heatmap_kws: Keyword args and values for seaborn's heatmap function.
    :param ax: Optional matplotlib axes to plot on.
    """
    matrix = create_transition_matrix(transitions=transitions, get_name=get_name,
                                      order_by=order_by, exclude=exclude)
    ax = ax or new_axes()
    if heatmap_kws is None:
        heatmap_kws = {}
    heatmap(matrix, ax=ax, **heatmap_kws, annot=True, fmt='0.0f')
    ax.set_xticklabels(matrix.columns.tolist())
    ax.set_yticklabels(matrix.columns.tolist())
    ax.invert_yaxis()
    ax.figure.tight_layout()
    return ax


def plot_markov_chain(transitions, get_location, get_name=None,
                      state_color=None, transition_color=None, arc_scale: float = 0.1,
                      text_kws: dict = None, circle_kws: dict = None, arrowstyle_kws: dict = None,
                      ax: Axes = None) -> Axes:
    """
    Plot a diagram of the Markov Chain corresponding to the given transitions between states.

    :param transitions: List of transitions and their counts or probabilities.
    :type transitions: Dict[Tuple[object, object], Union[float, int]]
    :param get_location: Lambda function to call to get state plot locations.
    :type get_location: Callable[[IUserAction], (float, float)]
    :param get_name: Optional lambda function to call to convert states to labels.
    :type get_name: Callable[[IUserAction], str]
    :param state_color: string or callable(state) to generate color for each state.
    :type state_color: Union[str, Callable]
    :param transition_color: string or callable(state) to generate color for each transition.
    :type transition_color: Union[str, Callable]
    :param arc_scale: this is multiplied by the distance between states to get the radius of the connecting arc
    :param text_kws: args to pass to `ax.text` for the state names
    :param circle_kws: args to pass to `matplotlib.patches.Circle` for the states
    :param arrowstyle_kws: args to pass to `matplotlib.patches.FancyArrowPatch(arrowstyle)` for the transitions
    :param ax: Optional matplotlib axes to plot on.
    """
    ax = ax or new_axes()
    circle_kws = circle_kws or {'radius': 0.35}
    text_kws = text_kws or {'ha': 'center', 'va': 'center'}
    get_name = get_name or str
    # get unique states
    states = set()
    for from_state, to_state in transitions.keys():
        states.update([from_state, to_state])
    # plot state circles
    for state in states:
        center = get_location(state)
        color = get_color(state_color, state, default='green')
        ax.add_patch(Circle(
            xy=center, color=color, **circle_kws
        ))
        ax.plot(*center, c='yellow')
    # plot transition arrows
    arrowstyle_kws = arrowstyle_kws or dict(stylename='Fancy', head_length=10, head_width=5, tail_width=2)
    for (from_state, to_state), number in transitions.items():
        from_center = get_location(from_state)
        to_center = get_location(to_state)
        distance = point_distance(from_center, to_center)
        circle_radius = circle_kws['radius']
        if distance > 0:
            from_edge = circle_edge(from_center, to_center, circle_radius, 15)
            to_edge = circle_edge(to_center, from_center, circle_radius, -15)
            color = get_color(transition_color, from_state, default='red')
            ax.add_patch(FancyArrowPatch(
                posA=from_edge, posB=to_edge,
                connectionstyle=ConnectionStyle(stylename='Arc3', rad=arc_scale*distance),
                arrowstyle=ArrowStyle(**arrowstyle_kws),
                linewidth=0, color=color
            ))
    # plot state labels
    for state in states:
        center = get_location(state)
        ax.text(*center, s=get_name(state), **text_kws)


def plot_sequence_diagram(sequence: IActionSequence, locations: List[str], max_grid_lines: int = 50) -> Axes:

    # calculate plot coordinates and labels
    data = sequence.map({
        'source': lambda act: act.source_id,
        'target': lambda act: act.target_id,
        'action-type': lambda act: act.action_type,
        'time-stamp': lambda act: act.time_stamp
    }).to_frame(wide=True)
    data['y_source'] = [
        len(locations) - locations.index(source) - 1
        if source in locations
        else len(locations)
        for source in data['source']
    ]
    data['y_target'] = [
        len(locations) - locations.index(target) - 1 if target in locations
        else None if target is None
        else len(locations)
        for target in data['target']
    ]
    data['source-label'] = [source if source not in locations else '' for source in data['source']]
    data['time-stamp_next'] = data['time-stamp'].shift(-1)
    # plot sequence
    ax = new_axes()
    t_min, t_max = data['time-stamp'].min(), data['time-stamp'].max()
    arrow_width = (t_max - t_min).total_seconds() / (200 * 24 * 60 * 60)
    #  labels
    for _, row in data.iterrows():
        x = row['time-stamp']
        y = row['y_source']
        # action arrows
        if row['y_target'] is not None:
            dy = row['y_target'] - row['y_source']
            print(x, y, dy)
            ax.arrow(x=x, y=y, dx=0, dy=dy,
                     width=arrow_width,
                     head_length=0.1, length_includes_head=True,
                     fc='#888888', ec='#444444',
                     zorder=-1)
        # source labels
        ax.text(x=row['time-stamp'], y=row['y_source'], s=row['source-label'],
                ha='center', va='bottom', rotation=45)
        # action labels
        y_text = (row['y_source'] + row['y_target']) / 2 if notnull(row['y_target']) else row['y_source']
        ax.text(x=row['time-stamp'] + timedelta(days=arrow_width), y=y_text, s=row['action-type'],
                ha='left', va='center', rotation=90)
        # actions
        ax.scatter(x, y, marker='D', color='k', zorder=1)
    #  format axes
    formatter = DateFormatter("%H:%M:%S")
    ax.xaxis.set_major_formatter(formatter)
    ax.set(
        yticks=arange(len(locations) + 1),
        yticklabels=(['other'] + locations)[:: -1]
    )
    ax.set_xlim(t_min - (t_max - t_min) / 10, t_max + (t_max - t_min) / 10)
    x_min, x_max = ax.get_xlim()
    min_spacing = (x_max - x_min) / max_grid_lines
    locators = [
        (1 / (24 * 60 * 60 * 12), SecondLocator(interval=1), SecondLocator(interval=1)),  # 5ms
        (1 / (24 * 60 * 60), SecondLocator(interval=1), SecondLocator(interval=5)),  # 1s
        (1 / (24 * 60 * 12), SecondLocator(interval=5), SecondLocator(interval=30)),  # 5s
        (1 / (24 * 60), MinuteLocator(interval=1), MinuteLocator(interval=5)),  # 1m
        (1 / (24 * 12), MinuteLocator(interval=5), HourLocator(interval=1)),  # 5m
        (1 / 24, HourLocator(interval=5), HourLocator(interval=6)),  # 1h
        (1, DayLocator(interval=1), DayLocator(interval=7)),  # 1d
        (7, DayLocator(interval=7), DayLocator(interval=30)),  # 1w
        (30, MonthLocator(interval=1), YearLocator()),  # 1M
    ]
    minor_locator = locators[-1][1]
    major_locator = locators[-1][2]
    for locator in locators[::-1]:
        if min_spacing < locator[0]:
            minor_locator = locator[1]
            major_locator = locator[2]
    ax.xaxis.set_minor_locator(minor_locator)
    ax.xaxis.set_major_locator(major_locator)
    ax.grid(which='minor', lw=0.5)
    ax.grid(which='major', lw=1)
    return ax
