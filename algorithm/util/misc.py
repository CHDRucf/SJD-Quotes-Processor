'''misc.py

Miscellaneous functionality used by the fuzzy search program.
Includes basic data manipulation and helper functions
'''

import itertools
import os
from typing import Iterable, Iterator, Tuple

from util.custom_types import (FlattenedQuotesDict, HeadwordQuotesDict,
                               MatchToMetadataDict)


def weighted_average(values_weights: Iterable[Tuple[float, float]]) -> float:
    '''
    Computes the weighted average of value-weight tuples. Each weight
    should be a fraction, and the sum of the weights should add up to 1

    Args:
        values_weights: An iterable of tuples, each consisting of a value
                        and its weight towards the total

    Returns:    The weighted sum of the given input values

    Raises:
        ValueError: If sum of value weights does not equal 1
    '''
    if sum([weight for _, weight in values_weights]) != 1:
        raise ValueError("Weights of values must add up 1")
    return sum(value * weight for value, weight in values_weights)


def flatten_quotes(headword_quotes: HeadwordQuotesDict) -> FlattenedQuotesDict:
    '''
    Converts the given dictionary of headwords to quote objects to
    a list of quote objects, with each quote modified
    to contain its associated headword

    Args:
        headword_quotes:    A dictionary of headwords each mapped to a list of
                            associated quotes

    Returns:    A "flattened" list of quotes. Each quote dictionary in this
                list contains its associated headword, mapped to the "headword'
                key
    '''
    return [{**quote, "headword": headword}
            for headword in headword_quotes for quote in headword_quotes[headword]]


def get_file_paths(top: str) -> Iterator[str]:
    '''
    Recursively finds all the filepaths starting from the specified
    directory.
    TODO: Filter the results so that only .txt files are returned?

    Args:
        top:    The directory to start searching from

    Returns:    An iterator with all the filepaths found
    '''
    return itertools.chain.from_iterable([file_names for _, _, file_names in os.walk(top)])


def get_top_five_matches_metadata(matches_metadata: MatchToMetadataDict) -> MatchToMetadataDict:
    '''
    Given a dictionary of match quotes each mapped to a dictionary
    representing their respective metadata, returns the top five mappings
    with the highest score value

    Args:
        matches_metadata:   The sentence-to-metadata dictionary

    Returns:    The top five sentence-to-metadata mappings with the highest
                scores
    '''
    return {
        key: value for key, value in
        sorted(matches_metadata.items(),
               key=lambda sentence_meta: sentence_meta[1].get('score'), reverse=True)[:5]
    }
