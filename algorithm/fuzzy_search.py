import logging
from collections import deque
from itertools import repeat
from multiprocessing import Pool
from typing import Deque, Iterator, List

from util.custom_types import Quote, QuoteMatch, WorkMetadata
from util.misc import chunks
from util.string_comp import fuzzy_search_over_corpora


def fuzzy_search_multiprocessed(quotes: List[Quote], work_metadatas: List[WorkMetadata],
                                corpora_path: str, num_processes: int,
                                chunk_size: int) -> List[QuoteMatch]:
    '''
    Performs a multiprocessed fuzzy search for the given quotes over the given
    corpora and returns a list of the results

    Args:
        quotes:         A list of quotes to search for
        work_metadatas: A list of work metadatas specifying the works to
                        search through
        corpora_path:   The path to the corpora home directory
        num_processes:  The number of processes to use for the search
        chunk_size:     The size of each quote chunk to perform multiprocessed
                        searching ont

    Returns:
        matches:    A list of the all matches found
    '''
    matches: Deque[QuoteMatch] = deque()
    quote_chunks: Iterator[List[Quote]] = chunks(quotes, chunk_size)
    i = 0
    with Pool(num_processes) as pool:
        for quote_chunk in quote_chunks:
            # TODO: If a work cannot be found, log an error message
            # and skip it instead of crashing
            top_fives: List[List[QuoteMatch]] = pool.starmap(
                fuzzy_search_over_corpora, zip(
                    quote_chunk,
                    repeat(work_metadatas),
                    repeat(corpora_path))
            )

            for top_five in top_fives:
                matches.extend(top_five)

            i += len(quote_chunk)
            logging.info(
                f"Finished searching for {i} / {len(quotes)} quote matches")

    return list(matches)
