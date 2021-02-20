'''test_string_cmp.py

Tests for the string_cmp module
'''

from typing import Any, List, Set

import pytest
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


@pytest.mark.parametrize(
    "quote, sentence, work, author, url",
    [
        (
            "That is, every thing is the better, the same, the fitter.  Sceptre and pow’r, "
            "thy giving, I assume; And glad her shall resign, when in the end Thou shalt be all "
            "in all, and I in thee, For ever; and in me all whom thou lov’st.",

            '''Scepter and Power, thy giving, I assume,
And gladlier shall resign, when in the end
Thou shalt be All in All, and I in thee
For ever, and in mee all whom thou lov’st:
But whom thou hat’st, I hate, and can put on
Thy terrors, as I put thy mildness on,
Image of thee in all things
and shall soon,
Armd with thy might, rid heav’n of these rebell’d,
To thir prepar’d ill Mansion driven down
To chains of Darkness, and th’ undying Worm,
That from thy just obedience could revolt,
Whom to obey is happiness entire.''',

            "Paradise Lost", "John Milton", "http://www.gutenberg.org/files/20/20-0.txt"
        ),
        (
            "Up with my tent, here will I lie to night; But where to morrow? —— Well, all’s one for that.",

            '''Up With my tent! Here will I lie to-night;
                      [Soldiers begin to set up the KING'S tent]
    But where to-morrow?''',

            "Richard III", "William Shakespeare", "http://www.gutenberg.org/cache/epub/1103/pg1103.txt"
        ),
        (
            "They that do not keep up this indifferency for all but truth, put coloured spectacles before their eyes, and look through false glasses.",

            "They that do not keep up this indifferency in themselves for all but truth, not supposed, but evidenced in themselves, put coloured spectacles before their eyes, and look on things through false glasses, and then think themselves excused in following the false appearances, which they themselves put upon them.",

            "The Works, vol. 2 An Essay concerning Human Understanding Part 2 and Other Writings", "John Locke", "https://oll.libertyfund.org/title/locke-the-works-vol-2-an-essay-concerning-human-understanding-part-2-and-other-writings"
        ),
        (
            "All the fitter, Lentulus: our coming Is not for salutation; we have bus’ness.",

            '''Why, all the fitter, LENTVLVS: our comming 200
195
189 you
185[Noise within.''',

            "Ben Jonson", "Catiline his conspiracy", "https://catalog.hathitrust.org/Record/001017535"
        )
    ])
def test_compare_quote_to_sentence(quote: str, sentence: str, work: str, author: str, url: str):
    TARGET_THRESHOLD = 0.9
    assert compare_quote_to_sentence(
        quote, sentence) > TARGET_THRESHOLD, f"Info:\nWork:   {work}\nAuthor: {author}\nURL:    {url}"
