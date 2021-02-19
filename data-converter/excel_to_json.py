'''excel_to_json.py
Functions for converting the sponsor-provided Excel spreadsheet
to JSON.
'''

import json
from collections import deque
from typing import Deque, List, NamedTuple

import pandas as pd


class QuoteMetadata(NamedTuple):
    headword: str
    edition: int
    definition: str
    quote: str
    title: str
    author: str


def excel_to_df(fn: str) -> pd.DataFrame:
    '''
    Reads the quote excel file and converts it to
    a Pandas DataFrame
    '''
    columns: list = ["HEAD", "EDITION", "POS", "DEFINITION",
                     "QUOTE", "TITLE", "AUTHOR", "BIBLSCOPE"]
    data: pd.DataFrame = pd.read_excel(fn, engine='xlrd')
    return pd.DataFrame(data, columns=columns)


def df_to_list(df: pd.DataFrame) -> List[QuoteMetadata]:
    '''
    Converts the Pandas DataFrame of the quote excel file
    to a list of QuoteMetadata namedtuples
    Prequisites:
        - The excel file must be formatted correctly
        - The headword of the first row in the file must not be empty
        - The edition number of the first row in the file must not be empty
        - The definition of the first row in the file must not be empty
        - The quote text of the first row in the file must must not be empty
    '''
    repeat_columns: list = ["HEAD", "EDITION", "DEFINITION", "QUOTE"]
    non_repeat_columns: list = ["TITLE", "POS", "AUTHOR", "BIBLSCOPE"]
    result: Deque[QuoteMetadata] = deque()
    metadata_for_this_quote: QuoteMetadata = {
        heading: "" for heading in repeat_columns}
    for tup in df.itertuples():

        # If the quote is null or whitespace, don't include it
        # This skips multiple editions of a quote that have the same text
        if pd.isnull(tup.QUOTE) or tup.QUOTE.strip() == "":
            continue

        # Handle the special case for the dictionary word "NULL"
        headword: str = tup.HEAD if not pd.isnull(tup.HEAD) else "NULL"

        for heading in repeat_columns:
            current_value: str = getattr(tup, heading)
            if not pd.isnull(current_value):
                metadata_for_this_quote[heading] = current_value

        for heading in non_repeat_columns:
            current_value: str = getattr(tup, heading)
            metadata_for_this_quote[heading] = "" if pd.isnull(
                current_value) else current_value

        metadata_for_this_quote["EDITION"] = int(
            metadata_for_this_quote["EDITION"])

        to_add: QuoteMetadata = QuoteMetadata(
            headword=headword,
            edition=metadata_for_this_quote["EDITION"],
            definition=metadata_for_this_quote["DEFINITION"],
            quote=metadata_for_this_quote["QUOTE"],
            title=metadata_for_this_quote["TITLE"],
            author=metadata_for_this_quote["AUTHOR"])

        result.append(to_add)
    return list(result)


def write_to_json(excel_fn: str, json_fn: str) -> List[QuoteMetadata]:
    '''
    Converts the Excel file with the name excel_fn to a Python
    dictionary and writes it to a JSON file with the name json_fn.

    Returns the quotes dictionary object when finished
    '''
    df: pd.DataFrame = excel_to_df(excel_fn)
    quotes: List[QuoteMetadata] = df_to_list(df)
    with open(json_fn, "w", encoding="utf-8") as fp:
        json.dump([quote._asdict() for quote in quotes],
                  fp, indent=4, ensure_ascii=False)

    return quotes
