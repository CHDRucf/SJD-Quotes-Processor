import pytest

from excel_to_json import df_to_dict, excel_to_df, quote_to_dict


def test_quote_to_dict():
    definition: str = "The first letter of the European alphabets, A, an article set before nouns of the singular number;  a man, a tree; denoting the number one, or an indefinite indication, A is sometimes a noun; A is placed before a participle, or participial noun; and is considered by Wallis as a contraction of  at, when it is put before a word denoting some action not yet finished;It also seems to be anciently contracted from at, when placed before local surnames;In other cases, it seems to signify to, like the French à. "
    assert quote_to_dict(1, definition, "A hunting Chloë went.", "", "Prior.") == {
        "edition": 1,
        "definition": "The first letter of the European alphabets, A, an article set before nouns of the singular number;  a man, a tree; denoting the number one, or an indefinite indication, A is sometimes a noun; A is placed before a participle, or participial noun; and is considered by Wallis as a contraction of  at, when it is put before a word denoting some action not yet finished;It also seems to be anciently contracted from at, when placed before local surnames;In other cases, it seems to signify to, like the French à. ",
        "quote": "A hunting Chloë went.",
        "title": "",
        "author": "Prior.",
        "flag": False
    }


def test_df_to_dict():
    fn: str = r"test.xlsx"
    df: object = excel_to_df(fn)

    result: dict = df_to_dict(df)
    expected: list = {
        "A": [
            {
                "edition": 1,
                "definition": "The first letter of the European alphabets, A, an article set before nouns of the singular number;  a man, a tree; denoting the number one, or an indefinite indication, A is sometimes a noun; A is placed before a participle, or participial noun; and is considered by Wallis as a contraction of  at, when it is put before a word denoting some action not yet finished;It also seems to be anciently contracted from at, when placed before local surnames;In other cases, it seems to signify to, like the French à. ",
                "quote": "A hunting Chloë went.",
                "title": "",
                "author": "Prior.",
                "flag": False
            },
            {
                "edition": 1,
                "definition": "The first letter of the European alphabets, A, an article set before nouns of the singular number;  a man, a tree; denoting the number one, or an indefinite indication, A is sometimes a noun; A is placed before a participle, or participial noun; and is considered by Wallis as a contraction of  at, when it is put before a word denoting some action not yet finished;It also seems to be anciently contracted from at, when placed before local surnames;In other cases, it seems to signify to, like the French à. ",
                "quote": "And now a breeze from shore began to blow, The sailors ship their oars, and cease to row; Then hoist their yards a-trip, and all their sails Let fall, to court the wind, and catch the gales.",
                "title": "Ceyx and Alcyone.",
                "author": "Dryden’s",
                "flag": False
            },
            {
                "edition": 4,
                "definition": "Letter 'a'",
                "quote": "And now a breeze from shore began to blow, The sailors ship their oars, and cease to row; Then hoist their yards a-trip, and all their sails Let fall, to court the wind, and catch the gales.",
                "title": "",
                "author": "",
                "flag": False
            },
        ]
    }
    assert result == expected
