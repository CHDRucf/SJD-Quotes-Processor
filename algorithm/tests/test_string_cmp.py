'''test_string_cmp.py

Tests for the string_cmp module
'''

from typing import List, Set

import pytest
from util.custom_types import Quote, QuoteMatch, WorkMetadata
from util.string_comp import (compare_quote_to_sentence,
                              fuzzy_search_over_file, jaccard_index)


@pytest.mark.parametrize(
    "set1, set2, expected",
    [
        ({1, 2, 3}, {4, 5, 6}, 0),
        ({1, 2, 3}, {3, 5, 6}, (1/5)),
        ({'c', 'a', 'r'}, {'b', 'a', 'r'}, (2/4)),
        ({'u', 'c', 'f'}, {'u', 's', 'f'}, (2/4))
    ]
)
def test_jaccard_index(set1: Set, set2: Set, expected: float):
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

            '''Why, all the fitter, Leutn!ns : our corning.
 Is not for falutation, we have bufmefs.''',

            "Ben Jonson", "Catiline his conspiracy", "https://babel.hathitrust.org/cgi/pt?id=uc2.ark:/13960/t84j0d39d&view=1up&seq=11"
        )
    ])
def test_compare_quote_to_sentence(quote: str, sentence: str, work: str, author: str, url: str):
    TARGET_THRESHOLD = 0.9
    assert compare_quote_to_sentence(
        quote, sentence) > TARGET_THRESHOLD, f"Info:\nWork:   {work}\nAuthor: {author}\nURL:    {url}"


@pytest.mark.parametrize(
    "quote, filepath, expected",
    [
        (
            "Up with my tent, here will I lie to night; But where to morrow? —— Well, all’s one for that.",
            "tests/test-txts/richard-iii.txt",
            "Up With my tent! Here will I lie to-night;"
        ),
        (
            "Dorset, your son, that with a fearful soul Leads discontented steps in foreign soil, This fair alliance quickly shall call home To high promotions.",
            "tests/test-txts/richard-iii.txt",
            "This fair alliance quickly shall can home"
        ),
        (
            "That is, every thing is the better, the same, the fitter.  Sceptre and pow’r, "
            "thy giving, I assume; And glad her shall resign, when in the end Thou shalt be all "
            "in all, and I in thee, For ever; and in me all whom thou lov’st.",
            "tests/test-txts/paradise-lost.txt",
            "Scepter and Power, thy giving, I assume,"
        ),
        (
            "This day, at height of noon, came to my sphere, A spirit, zealous, as he seem’d, to know More of the Almighty’s works.",
            "tests/test-txts/paradise-lost.txt",
            "A Spirit, zealous, as he seem’d, to know"
        ),
        (
            "As when the total kind  Of birds, in orderly array on wing, Came summon’d over Eden, to receive Their names of Thee.",
            "tests/test-txts/paradise-lost.txt",
            "Of Birds in orderly array on wing"
        ),
        (
            "Nor delay’d the winged saint, After his charge receiv’d; but from among Thousand celestial ardours, where he stood Veil’d with his gorgeous wings, up-springing light, Flew thro’ the midst of heav’n.",
            "tests/test-txts/paradise-lost.txt",
            "nor delaid the winged Saint"
        ),
        (
            "Up rose the victor angels, and to arms  The matin trumpet sung.",
            "tests/test-txts/paradise-lost.txt",
            "Up rose the Victor Angels, and to Arms"
        ),
        (
            "And now a breeze from shore began to blow, The sailors ship their oars, and cease to row; Then hoist their yards a-trip, and all their sails Let fall, to court the wind, and catch the gales.",
            "tests/test-txts/dryden-vol-12.txt",
            "And now a breeze from shore began to blow;"
        ),
        (
            "Your patrimonial stores in peace possess; Undoubted all your filial claim confess: Your private right should impious power invade, The peers of Ithaca would arm in aid.",
            "tests/test-txts/odyssey-pope.txt",
            "Your patrimonial stores in peace possess;"
        ),
        (
            "Aim’st thou at princes, all amaz’d they said, The last of games?",
            "tests/test-txts/odyssey-pope.txt",
            "Aim’st thou at princes"
        ),
        (
            "Crowds of rivals, for thy mother’s charms, Thy palace fill with insults and alarms.",
            "tests/test-txts/odyssey-pope.txt",
            "crowds of rivals"
        ),
        (
            "Say from what scepter’d ancestry ye claim, Recorded eminent in deathless fame?",
            "tests/test-txts/odyssey-pope.txt",
            "Say from what sceptred ancestry ye claim"
        ),
        (
            "Tall thriving trees confess’d the fruitful mold; The red’ning apple ripens here to gold.",
            "tests/test-txts/odyssey-pope.txt",
            "Tall thriving trees"
        ),
        (
            "Unmov’d the mind of Ithacus remain’d, And the vain ardours of our love restrain’d.",
            "tests/test-txts/odyssey-pope.txt",
            "Unmoved the mind of Ithacus remain’d;"
        )
    ]
)
def test_fuzzy_search_over_file(quote: str, filepath: str, expected: str):
    '''
    Assert that the expected substring is found in one of the top five
    matching quotes in the file
    '''
    text_file_string: str
    with open(filepath, "r", encoding="utf-8") as fp:
        text_file_string = fp.read()
    matches: List[QuoteMatch] = fuzzy_search_over_file(
        Quote(0, quote),
        WorkMetadata(0, "test", "test", "test", filepath, "test"),
        text_file_string
    )

    match_strings: List[str] = [m.content for m in matches]
    error_fmt: str = (
        "\n" + '-'*20 + "\n").join(f"'{ms}'" for ms in match_strings)
    assert any(
        expected in s for s in match_strings),\
        f"Expected text:\n'{expected}'" + "\n\nnot found in:\n\n" + error_fmt
