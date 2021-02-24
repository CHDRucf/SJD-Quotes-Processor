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
        # Richard III
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
            "Hath he set bounds between their love and me? I am their mother; who shall bar them from me?",
            "tests/test-txts/richard-iii.txt",
            "Hath he set bounds between"
        ),
        (
            "Give my voice on Richard’s side, To bar my master’s heirs in true descent! God knows I will not.",
            "tests/test-txts/richard-iii.txt",
            "give my voice on Richard's side"
        ),
        (
            "Sent before my time Into this breathing world, scarce half made up, And that so lamely and unfashionably, That dogs bark at me.",
            "tests/test-txts/richard-iii.txt",
            "sent before my time"
        ),
        (
            # This is probably a hard test; the dashes indicate skipped lines
            "Your beauty was the cause of that effect, Your beauty, that did haunt me in my sleep. ——  —— If I thought that, I tell thee, homicide, These nails should rend that beauty from my cheeks.",
            "tests/test-txts/richard-iii.txt",
            "Your beauty was the cause"
        ),
        # Paradise Lost
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
        # The Odyssey, Pope's Translation
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
        ),
        # Bible quotes; mostly easy
        (
            "And the angel of God called to Hagar out of heaven, and said unto her, what aileth thee, Hagar? fear not: for God hath heard the voice of the lad where he is.",
            "tests/test-txts/bible-kjv.txt",
            "to Hagar out of heaven"
        ),
        (
            "When the congregation is to be gathered together, you shall blow, but you shall not sound an alarm.",
            "tests/test-txts/bible-kjv.txt",
            "But when the congregation",
        ),
        (
            "Behold, God himself is with us for our captain, and his priests with sounding trumpets, to cry alarms against you.",
            "tests/test-txts/bible-kjv.txt",
            "behold, God himself is with us for our captain",
        ),
        (
            "They weighed for my price thirty pieces of silver.",
            "tests/test-txts/bible-kjv.txt",
            "They weighed for my price thirty pieces of silver",
        ),
        (
            # In the KJV translation it's spelled 'Jezebel'
            "Jezebeel painted her face and tired her head.",
            "tests/test-txts/bible-kjv.txt",
            "painted her face, and tired her head",
        ),
        (
            # This is a hard test, the quote is a big paraphrase
            "Nineveh repented at the preaching of Jonas.",
            "tests/test-txts/bible-kjv.txt",
            "they repented at the preaching of Jonas"
        ),
        (
            "Multiply and replenish the earth.",
            "tests/test-txts/bible-kjv.txt",
            "multiply, and replenish the earth,",
        ),
        (
            "Strong meat belongeth to them who, by reason of use, have their senses exercised to discern both good and evil.",
            "tests/test-txts/bible-kjv.txt",
            "strong meat belongeth to them",
        ),
        (
            # This may be a hard test, the original quote
            # is actually part of a longer sentence
            "A gift doth blind the eyes of the wise.",
            "tests/test-txts/bible-kjv.txt",
            "a gift doth blind the eyes of the wise",
        ),
        (
            "They knew him not, nor yet the voices of the prophets which are read every sabbath-day, they have fulfilled them in condemning him.",
            "tests/test-txts/bible-kjv.txt",
            "nor yet the voices of the prophets",
        ),
        # The Aeneid-Dryden quotes; mostly hard
        (
            # Part of a larger sentence
            "Defraud their clients, and, to lucre sold, Sit brooding on unprofitable gold, Who dare not give.",
            "tests/test-txts/aeneid-dryden.txt",
            "Defraud their clients, and, to lucre sold,"
        ),
        (
            "His former trembling once again renew’d, With acted fear the villain thus pursu’d.",
            "tests/test-txts/aeneid-dryden.txt",
            "His former trembling once again renew’d,"
        ),
        (
            "The conscious wretch must all his acts reveal; Loth to confess, unable to conceal; From the first moment of his vital breath, To his last hour of unrepenting death.",
            "tests/test-txts/aeneid-dryden.txt",
            "The conscious wretch must all his acts reveal,"
        ),
        (
            "Among the croud, but far above the rest, Young Turnus to the beauteous maid addrest.",
            "tests/test-txts/aeneid-dryden.txt",
            "Among the crowd, but far above the rest,"
        ),
        (
            # This is a hard test; SJ skipped a line in the original poem
            "Some strip the skin, some portion out the spoil, Some on the fire the reeking entrails broil.",
            "tests/test-txts/aeneid-dryden.txt",
            "Some strip the skin; some portion out the spoil;"
        ),
        # John Bull; easy and hard
        (
            "You have been bred to business; you can cipher: I wonder you never used your pen and ink.",
            "tests/test-txts/history-of-john-bull.txt",
            "cypher"
        ),
        (
            "I love exact dealing, and let Hocus audit, he knows how the money was disbursed.",
            "tests/test-txts/history-of-john-bull.txt",
            "I love exact dealing"
        ),
        (
            # Part of a longer sentence
            "They took great pleasure in compounding law-suits among their neighbours; for which they were the aversion of the gentlemen of the long robe.",
            "tests/test-txts/history-of-john-bull.txt",
            "great pleasure in compounding"
        ),
        (
            # Part of a longer sentence
            "John was the darling; he had all the good bits, was crammed with good pullet, chicken, and capon.",
            "tests/test-txts/history-of-john-bull.txt",
            "John was the darling: he had all the good bits"
        ),
        (
            # Very hard test; this quote is butchered from the original
            "There are few that know all the tricks of these lawyers; for aught I can see, your case is not a bit clearer than it was seven years ago.",
            "tests/test-txts/history-of-john-bull.txt",
            "know all the tricks and cheats of these"
        ),
        # King Lear, mostly easy
        (
            # Easy
            "I’ve seen the day, with my good biting faulchion, I would have made them skip.",
            "tests/test-txts/king-lear.txt",
            "with my good biting falchion"
        ),
        (
            # Part of a longer sentence
            "She hath abated me of half my train; Look’d black upon me.",
            "tests/test-txts/king-lear.txt",
            "She hath abated me of half my train"
        ),
        (
            # Middle of a longer sentence
            "Our pow’r Shall do a court’sy to our wrath, which men May blame, but not controul.",
            "tests/test-txts/king-lear.txt",
            "yet our power"
        ),
        (
            # Easy
            "See better, Lear, and let me still remain The true blank of thine.",
            "tests/test-txts/king-lear.txt",
            "See better, Lear, and let me still remain"
        ),
        (
            # Easy
            "You nimble lightnings, dart your blinding flames Into her scornful eyes!",
            "tests/test-txts/king-lear.txt",
            "You nimble lightnings"
        ),
        # Faerie Queene, Books I - VI
        # Seems to be mostly from books I and II, but all books included
        # in corpora to be safe. Lots of whitespace, few periods, and old English.
        # Probably very difficult
        # TODO: Update these tests to use excerpts from Hathi Trust txts
        (
            # Easy if whitespace is treated properly
            "Those foreigners which came from far Grew great, and got large portions of land, That in the realm, ere long, they stronger are Than they which sought at first their helping hand, And Vortiger enforced the kingdom to aband.",
            "tests/test-txts/the-faerie-queene--book-ii.txt",
            "And of those forreiners"
        ),
        (
            "It all above besprinkled was throughout With golden aigulets that glister’d bright, Like twinkling stars, and all the skirt about Was hemm’d with golden fringes.",
            "tests/test-txts/the-faerie-queene--book-ii.txt",
            "Which all aboue besprinckled"
        ),
        (
            "He boldly spake, Sir knight, if knight thou be,  Abandon this forestalled place at erst, For fear of further harm, I counsel thee.",
            "tests/test-txts/the-faerie-queene--book-ii.txt",
            "He boldly spake"
        ),
        (
            "There ancient night arriving, did alight  From her high weary waine.",
            "tests/test-txts/the-faerie-queene--book-i.txt",
            "auncient Night"
        ),
        (
            "And all within were walks and alleys wide, With footing worn, and leading inward far.",
            "tests/test-txts/the-faerie-queene--book-i.txt",
            "And all within were pathes",
        ),
        (
            "Then bad the knight this lady yede aloof,  And to an hill herself withdrew aside, From whence she might behold the battle’s proof, And else be safe from danger far descried.",
            "tests/test-txts/the-faerie-queene--book-i.txt",
            "bad the knight"
        ),
        (
            # Punctuation is wrong; may not pick up on second half
            "Therewith, amoved from his sober mood, And lives he yet, said he, that wrought this act? And do the heavens afford him vital food?",
            "tests/test-txts/the-faerie-queene--book-ii.txt",
            "And liues he yet"
        ),
        (
            "Yet swimming in that sea of blissful joy, He nought forgot.",
            "tests/test-txts/the-faerie-queene--book-i.txt",
            "Yet swimming in"
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
