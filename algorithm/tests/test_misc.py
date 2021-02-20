'''test_misc.py

Tests for the misc module
'''

from typing import List, Tuple

import pytest
from util.misc import chunks, weighted_average


def test_weighted_average():
    values_averages: List[Tuple[int, int]] = [
        ([(1, 0.5), (1, 0.5)], 1),
        ([(3, 0.15), (5, 0.5), (10, 0.05), (4, 0.3)], 4.65)
    ]
    for values, expected in values_averages:
        assert weighted_average(values) == expected


def test_weighted_average_raises_error():
    weights_do_not_add_up_to_1: List[Tuple[int, int]] = [
        (1, 0.5), (2, 0.3), (4, 0.6)
    ]
    with pytest.raises(ValueError):
        weighted_average(weights_do_not_add_up_to_1)


def test_chunks():
    xs: List[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    expected: List[List[int]] = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    assert expected == list(chunks(xs, 3))

    expected: List[List[int]] = [[1, 2], [3, 4, ], [5, 6], [7, 8], [9, 10]]
    assert expected == list(chunks(xs, 2))
