'''misc.py

Miscellaneous functionality used by the fuzzy search program.
Includes basic data manipulation and helper functions
'''

import json
import os
from util.custom_types import WorkMetadata
from typing import Iterable, Iterator, List, Tuple, TypeVar

T = TypeVar('T')


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


def get_filepaths(top: str) -> List[str]:
    '''
    Recursively finds all the filepaths starting from the specified
    directory. No longer used since filepaths are read from the metadata
    TODO: Filter the results so that only .txt files are returned?

    Args:
        top:    The directory to start searching from

    Returns:    An iterator with all the filepaths found
    '''
    result = []
    for dirpath, _, filenames in os.walk(top):
        result.extend(os.path.join(dirpath, filename)
                      for filename in filenames)
    return result

    # This also works, and may technically run faster, but is hardly legible
    # from itertools import chain, repeat, starmap
    # return list(chain.from_iterable(starmap(os.path.join, zip(repeat(dirpath), filenames))for dirpath, _, filenames in os.walk(top)))


def chunks(xs: List[T], n: int) -> Iterator[List[T]]:
    ''' Returns a copy of the list divided into chunks of size n'''
    return (xs[i:i+n] for i in range(0, len(xs), n))


def get_quick_lookup_works_for_author(quick_lookup_json_dir: str, works_list_json_fp: str):
    '''
    Gets all the work metadata for an author in the quick lookup list
    
    Args:
        quick_lookup_json_dir:  The directory containing the quick lookup JSONs
        works_list_json_fp:     The name of the JSON file containing a list of
                                filepaths to the author's works
    
    Returns:    A list of WorkMetadata objects representing all the works
                found by the given author
    '''
    with open(
            os.path.join(quick_lookup_json_dir, works_list_json_fp),
            "r", encoding="utf-8") as fp:
        content: dict = json.load(fp)
        return [WorkMetadata(**w) for w in content.get("data")]
