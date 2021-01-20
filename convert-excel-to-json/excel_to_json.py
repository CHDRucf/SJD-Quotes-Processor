import json

import pandas as pd


def excel_to_df(fn: str) -> pd.DataFrame:
    '''
    Reads the quote excel file and converts it to
    a Pandas DataFrame
    '''
    columns: list = ["HEAD", "EDITION", "POS", "DEFINITION",
               "QUOTE", "TITLE", "AUTHOR", "BIBLSCOPE"]
    data: object = pd.read_excel(fn)
    return pd.DataFrame(data, columns=columns)


def quote_to_dict(edition: int, definition: str, quote: str, title: str, author: str):
    '''
    Converts a quote with the given information into a
    Python dictionary object
    '''
    return {
        "edition": edition,
        "definition": definition,
        "quote": quote,
        "title": title,
        "author": author,
        "flag": False
    }


def df_to_dict(df: pd.DataFrame) -> dict:
    '''
    Converts the Pandas DataFrame of the quote excel file
    to a Python dictionary object
    Prequisites:
        - The excel file must be formatted correctly
        - The headword of the first row in the file must not be empty
        - The edition number of the first row in the file must not be empty
        - The definition of the first row in the file must not be empty
        - The quote text of the first row in the file must must not be empty
    '''
    repeat_columns = ["HEAD", "EDITION", "DEFINITION", "QUOTE"]
    non_repeat_columns = ["TITLE", "POS", "AUTHOR", "BIBLSCOPE"]
    result = dict()
    metadata_for_this_quote = {heading: "" for heading in repeat_columns}
    for tup in df.itertuples():
        if tup.HEAD not in result:
            result[tup.HEAD] = []

        for heading in repeat_columns:
            current_value = getattr(tup, heading)
            if not pd.isnull(current_value):
                metadata_for_this_quote[heading] = current_value

        for heading in non_repeat_columns:
            current_value = getattr(tup, heading)
            metadata_for_this_quote[heading] = "" if pd.isnull(
                current_value) else current_value

        metadata_for_this_quote["EDITION"] = int(
            metadata_for_this_quote["EDITION"])
        to_add = quote_to_dict(edition=metadata_for_this_quote["EDITION"],
                               definition=metadata_for_this_quote["DEFINITION"],
                               quote=metadata_for_this_quote["QUOTE"],
                               title=metadata_for_this_quote["TITLE"],
                               author=metadata_for_this_quote["AUTHOR"])

        result[tup.HEAD].append(to_add)
    return result


def main():
    fn = r"FullQuotes.xlsx"
    df = excel_to_df(fn)
    result = df_to_dict(df)
    with open("quotes.json", "w", encoding="utf-8") as fp:
        json.dump(result, fp, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
