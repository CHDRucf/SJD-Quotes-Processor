'''string_comp.py

Functions directly related to the fuzzy search algorithm's string comparison
metrics
'''

import operator
import os
import re
import string
from typing import List, Set

import Levenshtein

from util.custom_types import Quote, QuoteMatch, WorkMetadata
from util.misc import weighted_average


def split_by_punctuation(text: str) -> List[str]:
    '''
    TODO
    '''
    return re.split(r"[.!?]+", text)


def jaccard_index(set1: set, set2: set) -> float:
    ''' Computes the Jaccard Index between two sets'''
    return len(set1 & set2) / len(set1 | set2)


def compare_quote_to_sentence(quote: str, sentence: str) -> float:
    '''
    Compares a quote to a sentence and returns a normalized scalar value
    representing how similar they are. The two strings should all be in
    the matching case and have all punctuation removed beforehand

    Args:
        quote:      The quote to compare against the target sentence.
        sentence:   The sentence to be compared against

    Returns:
        result: The normalized scalar value representing how similar the
        quote is to the sentence. The closer to 1 this value is , the more
        similar the the quote and sentence are
    '''
    J_WEIGHT = 0.25
    L_WEIGHT = 0.75

    punc_replace_pattern = re.compile(re.escape(string.punctuation))

    # normalize quote string
    quote = quote.lower()
    quote = re.sub(punc_replace_pattern, "", quote)

    # normalize sentence string
    sentence = sentence.lower()
    sentence = re.sub(punc_replace_pattern, "", sentence)

    quote_set: Set[str] = set(quote)
    sentence_set: Set[str] = set(sentence)
    j_index: float = jaccard_index(quote_set, sentence_set)

    edit_distance: float = Levenshtein.ratio(quote, sentence)

    result = weighted_average([(j_index, J_WEIGHT), (edit_distance, L_WEIGHT)])

    return result


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

    # TODO: Implement this function
    sentences: List[str] = split_by_punctuation(text_file_string)

    # TODO: Implement logic to incrementally increase size of quote
    # for quotes with multiple sentences

    # Get all matches
    matches = [
        QuoteMatch(
            quote.id, work_metadata.id, 0,
            compare_quote_to_sentence(quote.content, s), s)
        for s in sentences
    ]

    # Return top five matches found
    return list(sorted(matches, key=operator.attrgetter("score"), reverse=True)[:5])


def fuzzy_search_over_corpora(quote: Quote, work_metadatas: List[WorkMetadata], corpora_path: str) -> List[QuoteMatch]:
    '''
    Performs a fuzzy search for a quote over a given corpora, represented as
    a list of file paths
    # TODO: Test

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

        with open(filepath, "r", encoding="utf-8") as fp:
            text_file_string: str = fp.read()

        top_five_matches_in_file: List[QuoteMatch] = fuzzy_search_over_file(
            quote, work_metadata, text_file_string)


        top_five_overall = list(
            sorted(
                top_five_matches_in_file + top_five_overall, key=operator.attrgetter("score"),
                reverse=True
            )[:5])

    return top_five_overall
