'''string_comp.py

Functions directly related to the fuzzy search algorithm's string comparison
metrics
'''

import operator
import os
import re
import string
from typing import Dict, List, Set

import Levenshtein
from mysql.connector.cursor import CursorBase

from util.custom_types import MatchToMetadataDict, Metadata
from util.database_ops import get_file_metadata
from util.misc import get_top_five_matches_metadata, weighted_average


def split_by_punctuation() -> List[str]:
    '''
    TODO
    '''
    ...


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

    quote_set: Set[str] = set(quote)
    sentence_set: Set[str] = set(sentence)
    j_index: float = jaccard_index(quote_set, sentence_set)

    edit_distance: float = Levenshtein.ratio(quote, sentence)

    result = weighted_average([(j_index, J_WEIGHT), (edit_distance, L_WEIGHT)])

    return result


def fuzzy_search_over_file(quote: str, text_file_string: str) -> Dict[str, float]:
    '''
    Performs a fuzzy search for a quote over the text contents of a given file

    Args:
        quote:              The quote to search for
        text_file_string:   The text contents of the file to search for
                            the quote in

    Returns:
        top_five:   A string-to-float dictionary containing the top five
                    matches found mapped to their scores
    '''
    punc_replace_pattern = re.compile(string.punctuation)

    # normalize quote string
    quote = quote.lower()
    quote = re.sub(punc_replace_pattern, "", quote)

    # normalize text file string
    text_file_string = text_file_string.lower()

    # TODO: Implement this function
    sentences: List[str] = split_by_punctuation()

    # TODO: Implement logic to incrementally increase size of quote
    # for quotes with multiple sentences

    possible_matches: Dict[str, float] = {}
    for sentence in sentences:
        sentence = re.sub(punc_replace_pattern, "", sentence)
        possible_matches[sentence] = compare_quote_to_sentence(quote, sentence)

    top_five: Dict[str, float] = {key: value for key, value in sorted(
        possible_matches.items(), key=operator.itemgetter(1), reverse=True)[:5]}

    return top_five


def fuzzy_search_over_corpora(quote: str, file_paths: List[str], cursor: CursorBase) -> MatchToMetadataDict:
    '''
    Performs a fuzzy search for a quote over a given corpora, represented as
    a list of file paths
    # TODO: Decouple this function from the database by replacing the cursor
    #       parameter with a list of file metadatum? Currently this function
    #       is the only one in this module that is tied to the database
    # TODO: Test

    Args:
        quote:      The quote to search for
        file_paths: A list of strings; each representing a file path to search
                    for the quote in

    Returns:
        top_five_overall:   A dictionary of string-to-dict values containing
                            the top five matches found mapped to their metadata
    '''
    top_five_overall: MatchToMetadataDict = {}

    for file_path in file_paths:
        _, file_name = os.path.split(file_path)

        metadata: Metadata = get_file_metadata(file_name, cursor)

        with open(file_path, "r") as fp:
            text_file_string: str = fp.read()

        top_five_in_file_scores: Dict[str, float] = fuzzy_search_over_file(
            quote, text_file_string)

        top_five_in_file_metadata: MatchToMetadataDict = {
            sentence: {**metadata, "score": score}
            for sentence, score in top_five_in_file_scores.items()
        }

        top_five_overall = get_top_five_matches_metadata(
            {**top_five_overall, **top_five_in_file_metadata})

    return top_five_overall
