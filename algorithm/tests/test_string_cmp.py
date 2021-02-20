'''test_string_cmp.py

Tests for the string_cmp module
'''

from typing import Any, List, Set

from util.string_comp import compare_quote_to_sentence, jaccard_index


def test_jaccard_index():
    sets_and_j_values: List[Set[Any]] = [
        ({1, 2, 3}, {4, 5, 6}, 0),
        ({1, 2, 3}, {3, 5, 6}, (1/5)),
        ({'c', 'a', 'r'}, {'b', 'a', 'r'}, (2/4)),
        ({'u', 'c', 'f'}, {'u', 's', 'f'}, (2/4))
    ]
    for set1, set2, expected in sets_and_j_values:
        assert jaccard_index(set1, set2) == expected


def test_compare_quote_to_sentence():
    for quote, sentence in [
        ("A hunting Chloë went.",
         "a hunting Chloe went"),
        ("They go a begging to a bankrupt’s door.",
         "they a go a beggin' to a bankrupts door"),
        ("May pure contents for ever pitch their tents Upon these downs, these meads, these rocks, these mountains, And peace still slumber by these purling fountains! Which we may every year Find when we come a fishing here.",
         "May pvre contents forever pitch there tents upon these downs, these meadows, these rocks, these mountains, And peece still slumber by these stirling fountains! which we may evr'y year find when we come a fishin' here."),
    ]:
        assert compare_quote_to_sentence(quote, sentence) > 0.9
