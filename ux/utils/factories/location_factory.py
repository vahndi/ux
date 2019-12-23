from typing import List, Iterator, Tuple


def one_shot(locations: List[str]) -> List[Tuple[str, str]]:
    """
    Generate a sequence of sources and targets that visits each location in turn.

    :return: List[Tuple[source, target]]
    """
    return [
        (locations[i_location], locations[i_location + 1])
        for i_location in range(len(locations) - 1)
    ]


def forward_back(locations: List[str], forwards: int, backwards: int) -> Iterator[Tuple[str, str]]:
    """
    Generate a sequence of sources and targets that goes forwards and backwards through the locations.

    :rtype: Iterator[Tuple[str, str]]
    :return: Iterator[Tuple[source, target]]
    """
    assert forwards > backwards, 'forwards must be greater than backwards'
    add_sequence = [1] * forwards + [-1] * backwards
    target = None
    i_source = 0
    sources_targets = []
    while target != locations[-1]:
        for add in add_sequence:
            source = locations[i_source]
            target = locations[i_source + add]
            i_source += add
            sources_targets.append((source, target))
            if target == locations[-1]:
                break
    return sources_targets
