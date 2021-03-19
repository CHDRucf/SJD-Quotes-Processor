'''string_comp.py
Functions directly related to the fuzzy search algorithm's string comparison
metrics
'''

import operator
import os
from collections import deque
from typing import Deque, List
import logging

import rapidfuzz

from util.custom_types import Quote, QuoteMatch, WorkMetadata


def fuzzy_search_over_file(quote: Quote, work_metadata: WorkMetadata, text_file_string: str) -> List[QuoteMatch]:
    '''
    Performs a fuzzy search for a quote over the text contents of a given file
    Args:
        quote:              The quote to search for
        work_metadata:      The metadata of the text file to search in
        text_file_string:   The text contents of the file to search for
                            the quote in
    Returns:    A list of the top five matches found
    '''

    window_size: int = len(quote.content)
    window_slide: int = window_size // 2
    sentences = [
        text_file_string[i:i+window_size]
        for i in range(0, len(text_file_string) - len(quote.content)//2, window_slide)
    ]

    matches = rapidfuzz.process.extract(
        quote.content, sentences, scorer=rapidfuzz.fuzz.ratio)

    top_five = sorted(matches, key=operator.itemgetter(1), reverse=True)[:5]

    results: Deque[QuoteMatch] = deque()
    # Expands the quote to be a sentence instead of an arbitrary substring
    for _, score, index in top_five:
        start: int = index * window_slide
        end: int = start + window_size
        end_punc: List[str] = ['.', '?', '!', ':']
        while start > 0 and text_file_string[start] not in end_punc:
            start -= 1
        while end < len(text_file_string) and text_file_string[end] not in end_punc:
            end += 1

        sentence = text_file_string[start:end]

        results.append(QuoteMatch(
            quote.id, work_metadata.id, 0, score, sentence))

    return list(results)


def fuzzy_search_over_corpora(quote: Quote, work_metadatas: List[WorkMetadata], corpora_path: str) -> List[QuoteMatch]:
    '''
    Performs a fuzzy search for a quote over a given corpora, represented as
    a list of file paths
    Args:
        quote:              The quote to search for
        work_metadatas:     A list of WorkMetadata objects, each containing
                            the path to their respective work
        corpora_path:       The The path to the directory in which the corpora are
                            located
    Returns:
        top_five_overall:   A list of the top five matches found
    '''
    top_five_overall: List[QuoteMatch] = []

    for work_metadata in work_metadatas:
        filepath = os.path.join(corpora_path, work_metadata.filepath)

        try:
            with open(filepath, "r", encoding="utf-8") as fp:
                text_file_string: str = fp.read()

            top_five_matches_in_file: List[QuoteMatch] = fuzzy_search_over_file(
                quote, work_metadata, text_file_string)

            top_five_overall = list(
                sorted(
                    top_five_matches_in_file + top_five_overall, key=operator.attrgetter("score"),
                    reverse=True
                )[:5])
        except FileNotFoundError:
            logging.warning(
                f"File at path '{filepath}' not found; searching skipped")

    return top_five_overall
