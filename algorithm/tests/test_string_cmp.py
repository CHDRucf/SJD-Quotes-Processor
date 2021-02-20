'''test_string_cmp.py

Tests for the string_cmp module
'''

from typing import Any, List, Set

from util.string_comp import jaccard_index


def test_jaccard_index():
    sets_and_j_values: List[Set[Any]] = [
        ({1, 2, 3}, {4, 5, 6}, 0),
        ({1, 2, 3}, {3, 5, 6}, (1/5)),
        ({'c', 'a', 'r'}, {'b', 'a', 'r'}, (2/4)),
        ({'u', 'c', 'f'}, {'u', 's', 'f'}, (2/4))
    ]
    for set1, set2, expected in sets_and_j_values:
        assert jaccard_index(set1, set2) == expected
