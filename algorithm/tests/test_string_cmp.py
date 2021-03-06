'''test_string_cmp.py

Tests for the string_cmp module
'''

from itertools import repeat
from typing import List

import pytest
from util.custom_types import Quote, QuoteMatch, WorkMetadata
from util.string_comp import fuzzy_search_over_corpora, fuzzy_search_over_file


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
        (
            # Hard, skips a line
            "Is not the causer of these timeless deaths, As blameful as the executioner?",
            "tests/test-txts/richard-iii.txt",
            "Is not the causer of"
        ),
        (
            "They that stand high, have many blasts to shake them; And, if they fall, they dash themselves to pieces.",
            "tests/test-txts/richard-iii.txt",
            "stand high have many blasts"
        ),
        (
            "Those eyes of thine from mine have drawn salt tears, Sham’d their aspects with store of childish drops.",
            "tests/test-txts/richard-iii.txt",
            "eyes of thine from mine"
        ),
        (
            "He wonders for what end you have assembled  Such troops of citizens to come to him.",
            "tests/test-txts/richard-iii.txt",
            "He wonders to what end you have assembled"
        ),
        # Paradise Lost
        (
            "That is, every thing is the better, the same, the fitter.  Sceptre and pow’r, thy giving, I assume; And glad her shall resign, when in the end Thou shalt be all in all, and I in thee, For ever; and in me all whom thou lov’st.",
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
            "the Victor Angels"
        ),
        (
            "The chief were those who, from the pit of hell Roaming to seek their prey on earth, durst fix Their seats long after next the seat of God.",
            "tests/test-txts/paradise-lost.txt",
            "chief were those who"
        ),
        (
            "Second of Satan sprung, all-conquering death! What think’st thou of our empire now?",
            "tests/test-txts/paradise-lost.txt",
            "Second of _Satan_ sprung"
        ),
        (
            # This one is funny: the headword is alliteration.
            # Instead of including the word in the quote, SJD
            # exemplified the word via the quote
            "Behemoth biggest born.",
            "tests/test-txts/paradise-lost.txt",
            "biggest born"
        ),
        (
            # Hard test: spelling is different for a few words
            "The great luminary  Aloft the vulgar constellations thick, That from his lordly eye keep distance due Dispenses light from far.",
            "tests/test-txts/paradise-lost.txt",
            "the great Luminarie"
        ),
        (
            "In their palaces, Where luxury late reign’d, sea-monsters whelp’d  And stabled.",
            "tests/test-txts/paradise-lost.txt",
            "Sea-monsters"
        ),
        # Iliads, Chapman's Translation
        (
            "Three binders stood, and took the handfuls reapt From boys that gather’d quickly up.",
            "tests/test-txts/iliads-chapman.txt",
            "binders stood,"
        ),
        (
            "Out rusht, with unmeasur’d roar, Those two winds, tumbling clouds in heaps; ushers to either’s blore.",
            "tests/test-txts/iliads-chapman.txt",
            "Those two Winds"
        ),
        (
            # Part of a larger sentence
            "I much fear, left with the blows of flies, His brass inflicted wounds are fill’d.",
            "tests/test-txts/iliads-chapman.txt",
            "I much fear"
        ),
        (
            "All fell upon the high-hair’d oaks, and down their curled brows Fell bustling to the earth; and up went all the boles and boughs.",
            "tests/test-txts/iliads-chapman.txt",
            "All fell upon the high-hair’d"
        ),
        (
            "I’ll burst him; I will bray  His bones as in a mortar.",
            "tests/test-txts/iliads-chapman.txt",
            "I’ll burst him"
        ),
        (
            "Fresh garlands too, the virgin’s temples crown’d; The youth’s gilt swords wore at their thighs, with silver bawdricks bound.",
            "tests/test-txts/iliads-chapman.txt",
            "Fresh garlands"
        ),
        (
            "In their sides, arms, shoulders, all bepincht,  Ran thick the weals, red with blood, ready to start out.",
            "tests/test-txts/iliads-chapman.txt",
            "all bepinch’d"
        ),
        (
            "Both fill’d with dust, but starting up, the third close they had made, Had not Achilles’ self stood up.",
            "tests/test-txts/iliads-chapman.txt",
            "Both fil’d with dust"
        ),
        (
            "Lion like, uplandish and more wild, Slave to his pride, and all his nerves being naturally compil’d  Of eminent strength, stalks out and preys upon a silly sheep.",
            "tests/test-txts/iliads-chapman.txt",
            "lion-like, uplandish"
        ),
        (
            "Words her worth had prov’d with deeds, Had more ground been allow’d the race, and coted far his steeds.",
            "tests/test-txts/iliads-chapman.txt",
            "words her worth"
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
        (
            "My friend, indulge one labour more, And seek Atrides.",
            "tests/test-txts/odyssey-pope.txt",
            "indulge one labour more"
        ),
        (
            "In vain they strive; th' intangling snares deny,  Inextricably firm, the power to fly.",
            "tests/test-txts/odyssey-pope.txt",
            "In vain they strive"
        ),
        (
            "While life informs these limbs, the king reply'd, Well to deserve be all my cares employ'd.",
            "tests/test-txts/odyssey-pope.txt",
            "While life informs these"
        ),
        (
            # Ending of a longer sentence
            "Perfidious and ingrate!  His stores ye ravage, and usurp his state.",
            "tests/test-txts/odyssey-pope.txt",
            "perfidious and ingrate"
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
            "congregation is to be"
        ),
        (
            "Behold, God himself is with us for our captain, and his priests with sounding trumpets, to cry alarms against you.",
            "tests/test-txts/bible-kjv.txt",
            "behold, God himself is with us for our captain",
        ),
        (
            "They weighed for my price thirty pieces of silver.",
            "tests/test-txts/bible-kjv.txt",
            "my price thirty pieces"
        ),
        (
            # In the KJV translation it's spelled 'Jezebel'
            "Jezebeel painted her face and tired her head.",
            "tests/test-txts/bible-kjv.txt",
            "tired her head"
        ),
        (
            # This is a hard test, the quote is a big paraphrase
            "Nineveh repented at the preaching of Jonas.",
            "tests/test-txts/bible-kjv.txt",
            "at the preaching of Jonas"
        ),
        (
            "Multiply and replenish the earth.",
            "tests/test-txts/bible-kjv.txt",
            "and replenish the earth,"
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
            "gift doth"
        ),
        (
            "They knew him not, nor yet the voices of the prophets which are read every sabbath-day, they have fulfilled them in condemning him.",
            "tests/test-txts/bible-kjv.txt",
            "nor yet the voices of the prophets",
        ),
        # The Aeneid-Dryden quotes; first five mostly hard
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
        (
            "What hopes you had in Diomede, lay down; Our hopes must centre on ourselves alone.",
            "tests/test-txts/aeneid-dryden.txt",
            "you had in Diomedes"
        ),
        (
            "In this high temple, on a chair of state, The seat of audience, old Latinus sate.",
            "tests/test-txts/aeneid-dryden.txt",
            "In this high temple"
        ),
        (
            "The spear flew hissing through the middle space, And pierc’d his throat, directed at his face.",
            "tests/test-txts/aeneid-dryden.txt",
            "flew hissing thro’"
        ),
        (
            "He calls the gods to witness their offence;  Disclaims the war, asserts his innocence.",
            "tests/test-txts/aeneid-dryden.txt",
            "He calls the gods to witness their offence,"
        ),
        (
            "Dauntless he rose, and to the fight return’d: With shame his glowing cheeks, his eyes with fury burn’d.",
            "tests/test-txts/aeneid-dryden.txt",
            "he rose, and to the fight"
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
        (
            "He skipped from room to room, ran up stairs and down stairs, from the kitchen to the garrets, and he peeped into every cranny.",
            "tests/test-txts/history-of-john-bull.txt",
            "skipped from room to room"
        ),
        (
            "He was hardly able to crawl about the room, far less to look after a troublesome business.",
            "tests/test-txts/history-of-john-bull.txt",
            "crawl about the room"
        ),
        (
            "He settled him in a good creditable way of living, having procured him by his interest one of the best places of the country.",
            "tests/test-txts/history-of-john-bull.txt",
            "good creditable way"
        ),
        (
            "The evidence is crimp; the witnesses swear backwards and forwards, and contradict themselves; and his tenants stick by him.",
            "tests/test-txts/history-of-john-bull.txt",
            "evidence is crimp"
        ),
        (
            "She was none of your cross-grained, termagant, scolding jades, that one had as good be hanged as live in the house with.",
            "tests/test-txts/history-of-john-bull.txt",
            "none of your cross-grained"
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
        (
            "Thou but remember’st me of my own conception. I have perceived a most faint neglect of late; which I have rather blamed as my own jealous curiosity, than as a very pretence and purpose of unkindness.",
            "tests/test-txts/king-lear.txt",
            "Thou but rememb'rest"
        ),
        (
            "The best and soundest of his time hath been but rash: now must we look, from his age, to receive not alone the imperfections of long engrafted condition, but therewithal the unruly waywardness that infirm and cholerick years bring with them.",
            "tests/test-txts/king-lear.txt",
            "The best and soundest"
        ),
        (
            "You are old: Nature in you stands on the very verge Of her confine.",
            "tests/test-txts/king-lear.txt",
            "Nature in you stands"
        ),
        (
            "It pleas’d the king his master to strike at me, When he, conjunct and flatt’ring his displeasure, Tript me behind.",
            "tests/test-txts/king-lear.txt",
            "It pleas'd the King his master very late"
        ),
        (
            "Of my land, Loyal and natural boy! I’ll work the means To make thee capable.",
            "tests/test-txts/king-lear.txt",
            "and of my land"
        ),
        # Faerie Queene, Books I - VI
        # Seems to be mostly from books I and II, but all books included
        # in corpora to be safe. Lots of whitespace, few periods, and old English.
        # Probably very difficult
        # TODO: Update these tests to use excerpts from Hathi Trust txts
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
        ),
        (
            "He, now to prove his late renewed might, High-brandishing his bright dew-burning blade, Upon his crested scalp so sore did smite, That to the scull a yawning wound it made.",
            "tests/test-txts/the-faerie-queene--book-i.txt",
            "He, now to proue"
        ),
        (
            "So both to battle fierce arranged are; In which his harder fortune was to fall Under my spear: such is the die of war.",
            "tests/test-txts/the-faerie-queene--book-i.txt",
            "both to battell fierce"
        ),
        (
            # Easy if whitespace is treated properly
            "Those foreigners which came from far Grew great, and got large portions of land, That in the realm, ere long, they stronger are Than they which sought at first their helping hand, And Vortiger enforced the kingdom to aband.",
            "tests/test-txts/the-faerie-queene--book-ii.txt",
            "of those forreiners"
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
        # Henry IV, parts 1 and 2
        (
            "This same half-faced fellow, Shadow; give me this man: he presents no mark to the enemy: the foeman may with as great aim level at the edge of a penknife.",
            "tests/test-txts/henry-iv-2.txt",
            "half-fac'd fellow"
        ),
        (
            "The king himself in person hath set forth, Or hitherwards intended speedily, With strong and mighty preparation.",
            "tests/test-txts/henry-iv-1.txt",
            "hitherwards intended speedily"
        ),
        (
            "To the English court assemble now, From ev'ry region, apes of idleness.",
            "tests/test-txts/henry-iv-2.txt",
            "English court assemble"
        ),
        (
            "Prince Harry is valiant; for the cold blood he did naturally inherit of his father he hath, like lean, steril land, manured with excellent good store of fertile sherris.",
            "tests/test-txts/henry-iv-2.txt",
            "Prince Harry is valiant"
        ),
        (
            "The skipping king, he rambled up and down With shallow jesters, and rash bavin wits; Soon kindled, and soon burnt.",
            "tests/test-txts/henry-iv-1.txt",
            "The skipping King"
        ),
        (
            "Thou knowest I am as valiant as Hercules; but beware instinct; the lion will not touch the true prince: instinct is a great matter. I was a coward on instinct: I shall think the better of myself and thee, during my life; I for a valiant lion, and thee for a true prince.",
            "tests/test-txts/henry-iv-1.txt",
            "I am as valiant as Hercules"
        ),
        (
            "Who hath not heard it spoken How deep you were within the books of heav'n? To us, th' imagin'd voice of heav'n itself; The very opener and intelligencer  Between the grace and sanctities of heav'n, And our dull workings.",
            "tests/test-txts/henry-iv-2.txt",
            "the books of God"
        ),
        (
            "If that rebellion Came like itself, in base and abject routs; I say, if damn'd commotion so appear'd, In his true, native, and most proper shape, You, reverend father, and these noble lords, Had not been here.",
            "tests/test-txts/henry-iv-2.txt",
            "in base and abject routs"
        ),
        (
            "There is a history in all mens lives, Figuring the nature of the times deceas'd; The which observ'd, a man may prophesy, With a near aim, of the main chance of things As yet not come to life, which in their seeds And weak beginnings he intreasured.",
            "tests/test-txts/henry-iv-2.txt",
            "history in all men's lives"
        ),
        (
            "Look you, all you that kiss my lady peace at home, that our armies join not in a hot day.",
            "tests/test-txts/henry-iv-2.txt",
            "kiss my Lady Peace"
        ),
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


quotes = [
    "Up with my tent, here will I lie to night; But where to morrow? —— Well, all’s one for that.",
    "Dorset, your son, that with a fearful soul Leads discontented steps in foreign soil, This fair alliance quickly shall call home To high promotions.",
    "Hath he set bounds between their love and me? I am their mother; who shall bar them from me?",
    "Give my voice on Richard’s side, To bar my master’s heirs in true descent! God knows I will not.",
    "Sent before my time Into this breathing world, scarce half made up, And that so lamely and unfashionably, That dogs bark at me.",
    "Your beauty was the cause of that effect, Your beauty, that did haunt me in my sleep. ——  —— If I thought that, I tell thee, homicide, These nails should rend that beauty from my cheeks.",
    "Is not the causer of these timeless deaths, As blameful as the executioner?",
    "They that stand high, have many blasts to shake them; And, if they fall, they dash themselves to pieces.",
    "Those eyes of thine from mine have drawn salt tears, Sham’d their aspects with store of childish drops.",
    "He wonders for what end you have assembled  Such troops of citizens to come to him.",
    "That is, every thing is the better, the same, the fitter.  Sceptre and pow’r, thy giving, I assume; And glad her shall resign, when in the end Thou shalt be all in all, and I in thee, For ever; and in me all whom thou lov’st.",
    "This day, at height of noon, came to my sphere, A spirit, zealous, as he seem’d, to know More of the Almighty’s works.",
    "As when the total kind  Of birds, in orderly array on wing, Came summon’d over Eden, to receive Their names of Thee.",
    "Nor delay’d the winged saint, After his charge receiv’d; but from among Thousand celestial ardours, where he stood Veil’d with his gorgeous wings, up-springing light, Flew thro’ the midst of heav’n.",
    "Up rose the victor angels, and to arms  The matin trumpet sung.",
    "The chief were those who, from the pit of hell Roaming to seek their prey on earth, durst fix Their seats long after next the seat of God.",
    "Second of Satan sprung, all-conquering death! What think’st thou of our empire now?",
    "Behemoth biggest born.",
    "The great luminary  Aloft the vulgar constellations thick, That from his lordly eye keep distance due Dispenses light from far.",
    "In their palaces, Where luxury late reign’d, sea-monsters whelp’d  And stabled.",
    "Three binders stood, and took the handfuls reapt From boys that gather’d quickly up.",
    "Out rusht, with unmeasur’d roar, Those two winds, tumbling clouds in heaps; ushers to either’s blore.",
    "I much fear, left with the blows of flies, His brass inflicted wounds are fill’d.",
    "All fell upon the high-hair’d oaks, and down their curled brows Fell bustling to the earth; and up went all the boles and boughs.",
    "I’ll burst him; I will bray  His bones as in a mortar.",
    "Fresh garlands too, the virgin’s temples crown’d; The youth’s gilt swords wore at their thighs, with silver bawdricks bound.",
    "In their sides, arms, shoulders, all bepincht,  Ran thick the weals, red with blood, ready to start out.",
    "Both fill’d with dust, but starting up, the third close they had made, Had not Achilles’ self stood up.",
    "Lion like, uplandish and more wild, Slave to his pride, and all his nerves being naturally compil’d  Of eminent strength, stalks out and preys upon a silly sheep.",
    "Words her worth had prov’d with deeds, Had more ground been allow’d the race, and coted far his steeds.",
    "Your patrimonial stores in peace possess; Undoubted all your filial claim confess: Your private right should impious power invade, The peers of Ithaca would arm in aid.",
    "Aim’st thou at princes, all amaz’d they said, The last of games?",
    "Crowds of rivals, for thy mother’s charms, Thy palace fill with insults and alarms.",
    "Say from what scepter’d ancestry ye claim, Recorded eminent in deathless fame?",
    "Tall thriving trees confess’d the fruitful mold; The red’ning apple ripens here to gold.",
    "Unmov’d the mind of Ithacus remain’d, And the vain ardours of our love restrain’d.",
    "My friend, indulge one labour more, And seek Atrides.",
    "In vain they strive; th' intangling snares deny,  Inextricably firm, the power to fly.",
    "While life informs these limbs, the king reply'd, Well to deserve be all my cares employ'd.",
    "Perfidious and ingrate!  His stores ye ravage, and usurp his state.",
    "And the angel of God called to Hagar out of heaven, and said unto her, what aileth thee, Hagar? fear not: for God hath heard the voice of the lad where he is.",
    "When the congregation is to be gathered together, you shall blow, but you shall not sound an alarm.",
    "Behold, God himself is with us for our captain, and his priests with sounding trumpets, to cry alarms against you.",
    "They weighed for my price thirty pieces of silver.",
    "Jezebeel painted her face and tired her head.",
    "Nineveh repented at the preaching of Jonas.",
    "Multiply and replenish the earth.",
    "Strong meat belongeth to them who, by reason of use, have their senses exercised to discern both good and evil.",
    "A gift doth blind the eyes of the wise.",
    "They knew him not, nor yet the voices of the prophets which are read every sabbath-day, they have fulfilled them in condemning him.",
    "Defraud their clients, and, to lucre sold, Sit brooding on unprofitable gold, Who dare not give.",
    "His former trembling once again renew’d, With acted fear the villain thus pursu’d.",
    "The conscious wretch must all his acts reveal; Loth to confess, unable to conceal; From the first moment of his vital breath, To his last hour of unrepenting death.",
    "Among the croud, but far above the rest, Young Turnus to the beauteous maid addrest.",
    "Some strip the skin, some portion out the spoil, Some on the fire the reeking entrails broil.",
    "What hopes you had in Diomede, lay down; Our hopes must centre on ourselves alone.",
    "In this high temple, on a chair of state, The seat of audience, old Latinus sate.",
    "The spear flew hissing through the middle space, And pierc’d his throat, directed at his face.",
    "He calls the gods to witness their offence;  Disclaims the war, asserts his innocence.",
    "Dauntless he rose, and to the fight return’d: With shame his glowing cheeks, his eyes with fury burn’d.",
    "You have been bred to business; you can cipher: I wonder you never used your pen and ink.",
    "I love exact dealing, and let Hocus audit, he knows how the money was disbursed.",
    "They took great pleasure in compounding law-suits among their neighbours; for which they were the aversion of the gentlemen of the long robe.",
    "John was the darling; he had all the good bits, was crammed with good pullet, chicken, and capon.",
    "There are few that know all the tricks of these lawyers; for aught I can see, your case is not a bit clearer than it was seven years ago.",
    "He skipped from room to room, ran up stairs and down stairs, from the kitchen to the garrets, and he peeped into every cranny.",
    "He was hardly able to crawl about the room, far less to look after a troublesome business.",
    "He settled him in a good creditable way of living, having procured him by his interest one of the best places of the country.",
    "The evidence is crimp; the witnesses swear backwards and forwards, and contradict themselves; and his tenants stick by him.",
    "She was none of your cross-grained, termagant, scolding jades, that one had as good be hanged as live in the house with.",
    "I’ve seen the day, with my good biting faulchion, I would have made them skip.",
    "She hath abated me of half my train; Look’d black upon me.",
    "Our pow’r Shall do a court’sy to our wrath, which men May blame, but not controul.",
    "See better, Lear, and let me still remain The true blank of thine.",
    "You nimble lightnings, dart your blinding flames Into her scornful eyes!",
    "Thou but remember’st me of my own conception. I have perceived a most faint neglect of late; which I have rather blamed as my own jealous curiosity, than as a very pretence and purpose of unkindness.",
    "The best and soundest of his time hath been but rash: now must we look, from his age, to receive not alone the imperfections of long engrafted condition, but therewithal the unruly waywardness that infirm and cholerick years bring with them.",
    "You are old: Nature in you stands on the very verge Of her confine.",
    "It pleas’d the king his master to strike at me, When he, conjunct and flatt’ring his displeasure, Tript me behind.",
    "Of my land, Loyal and natural boy! I’ll work the means To make thee capable.",
    "There ancient night arriving, did alight  From her high weary waine.",
    "And all within were walks and alleys wide, With footing worn, and leading inward far.",
    "Then bad the knight this lady yede aloof,  And to an hill herself withdrew aside, From whence she might behold the battle’s proof, And else be safe from danger far descried.",
    "Therewith, amoved from his sober mood, And lives he yet, said he, that wrought this act? And do the heavens afford him vital food?",
    "Yet swimming in that sea of blissful joy, He nought forgot.",
    "He, now to prove his late renewed might, High-brandishing his bright dew-burning blade, Upon his crested scalp so sore did smite, That to the scull a yawning wound it made.",
    "So both to battle fierce arranged are; In which his harder fortune was to fall Under my spear: such is the die of war.",
    "Those foreigners which came from far Grew great, and got large portions of land, That in the realm, ere long, they stronger are Than they which sought at first their helping hand, And Vortiger enforced the kingdom to aband.",
    "It all above besprinkled was throughout With golden aigulets that glister’d bright, Like twinkling stars, and all the skirt about Was hemm’d with golden fringes.",
    "He boldly spake, Sir knight, if knight thou be,  Abandon this forestalled place at erst, For fear of further harm, I counsel thee.",
    "This same half-faced fellow, Shadow; give me this man: he presents no mark to the enemy: the foeman may with as great aim level at the edge of a penknife.",
    "The king himself in person hath set forth, Or hitherwards intended speedily, With strong and mighty preparation.",
    "To the English court assemble now, From ev'ry region, apes of idleness.",
    "Prince Harry is valiant; for the cold blood he did naturally inherit of his father he hath, like lean, steril land, manured with excellent good store of fertile sherris.",
    "The skipping king, he rambled up and down With shallow jesters, and rash bavin wits; Soon kindled, and soon burnt.",
    "Thou knowest I am as valiant as Hercules; but beware instinct; the lion will not touch the true prince: instinct is a great matter. I was a coward on instinct: I shall think the better of myself and thee, during my life; I for a valiant lion, and thee for a true prince.",
    "Who hath not heard it spoken How deep you were within the books of heav'n? To us, th' imagin'd voice of heav'n itself; The very opener and intelligencer  Between the grace and sanctities of heav'n, And our dull workings.",
    "If that rebellion Came like itself, in base and abject routs; I say, if damn'd commotion so appear'd, In his true, native, and most proper shape, You, reverend father, and these noble lords, Had not been here.",
    "There is a history in all mens lives, Figuring the nature of the times deceas'd; The which observ'd, a man may prophesy, With a near aim, of the main chance of things As yet not come to life, which in their seeds And weak beginnings he intreasured.",
    "Look you, all you that kiss my lady peace at home, that our armies join not in a hot day."
]

works_metadatas = [
    WorkMetadata(0, "Test", "Test", "Test", "aeneid-dryden.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test", "bible-kjv.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test", "henry-iv-1.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test", "henry-iv-2.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test",
                 "history-of-john-bull.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test", "iliads-chapman.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test", "king-lear.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test", "odyssey-pope.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test", "paradise-lost.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test", "richard-iii.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test",
                 "the-faerie-queene--book-i.txt", "Test"),
    WorkMetadata(0, "Test", "Test", "Test",
                 "the-faerie-queene--book-ii.txt", "Test"),
]

expected = [
    "Up With my tent! Here will I lie to-night;",
    "This fair alliance quickly shall can home",
    "Hath he set bounds between",
    "give my voice on Richard's side",
    "sent before my time",
    "Your beauty was the cause",
    "Is not the causer of",
    "stand high have many blasts",
    "eyes of thine from mine",
    "He wonders to what end you have assembled",
    "Scepter and Power, thy giving, I assume,",
    "A Spirit, zealous, as he seem’d, to know",
    "Of Birds in orderly array on wing",
    "nor delaid the winged Saint",
    "the Victor Angels",
    "chief were those who",
    "Second of _Satan_ sprung",
    "biggest born",
    "the great Luminarie",
    "Sea-monsters",
    "binders stood,",
    "Those two Winds",
    "I much fear",
    "All fell upon the high-hair’d",
    "I’ll burst him",
    "Fresh garlands",
    "all bepinch’d",
    "Both fil’d with dust",
    "lion-like, uplandish",
    "words her worth",
    "Your patrimonial stores in peace possess;",
    "Aim’st thou at princes",
    "crowds of rivals",
    "Say from what sceptred ancestry ye claim",
    "Tall thriving trees",
    "Unmoved the mind of Ithacus remain’d;",
    "indulge one labour more",
    "In vain they strive",
    "While life informs these",
    "perfidious and ingrate",
    "to Hagar out of heaven",
    "congregation is to be",
    "behold, God himself is with us for our captain",
    "my price thirty pieces",
    "tired her head",
    "at the preaching of Jonas",
    "and replenish the earth,",
    "strong meat belongeth to them",
    "gift doth",
    "nor yet the voices of the prophets",
    "Defraud their clients, and, to lucre sold,",
    "His former trembling once again renew’d,",
    "The conscious wretch must all his acts reveal,",
    "Among the crowd, but far above the rest,",
    "Some strip the skin; some portion out the spoil;",
    "you had in Diomedes",
    "In this high temple",
    "flew hissing thro’",
    "He calls the gods to witness their offence,",
    "he rose, and to the fight",
    "cypher",
    "I love exact dealing",
    "great pleasure in compounding",
    "John was the darling: he had all the good bits",
    "know all the tricks and cheats of these",
    "skipped from room to room",
    "crawl about the room",
    "good creditable way",
    "evidence is crimp",
    "none of your cross-grained",
    "with my good biting falchion",
    "She hath abated me of half my train",
    "yet our power",
    "See better, Lear, and let me still remain",
    "You nimble lightnings",
    "Thou but rememb'rest",
    "The best and soundest",
    "Nature in you stands",
    "It pleas'd the King his master very late",
    "and of my land",
    "auncient Night",
    "And all within were pathes",
    "bad the knight",
    "And liues he yet",
    "Yet swimming in",
    "He, now to proue",
    "both to battell fierce",
    "of those forreiners",
    "Which all aboue besprinckled",
    "He boldly spake",
    "half-fac'd fellow",
    "hitherwards intended speedily",
    "English court assemble",
    "Prince Harry is valiant",
    "The skipping King",
    "I am as valiant as Hercules",
    "the books of God",
    "in base and abject routs",
    "history in all men's lives",
    "kiss my Lady Peace"
]


@pytest.mark.parametrize(
    "quote, works_metadatas, expected",
    zip(quotes, repeat(works_metadatas), expected)
)
def test_fuzzy_search_over_corpora(quote: str, works_metadatas: List[WorkMetadata], expected: str):
    matches: List[QuoteMatch] = fuzzy_search_over_corpora(
        Quote(0, quote), works_metadatas, "tests/test-txts/")

    match_strings: List[str] = [m.content for m in matches]
    error_fmt: str = (
        "\n" + '-'*20 + "\n").join(f"'{ms}'" for ms in match_strings)

    assert any(
        expected in s for s in match_strings),\
        f"Expected text:\n'{expected}'" + "\n\nnot found in:\n\n" + error_fmt
