import logging
from collections import deque
from itertools import repeat
from multiprocessing import Pool
from typing import Deque, Dict, Iterator, List, Tuple

from util.custom_types import AuthorQuoteWork, Quote, QuoteMatch, WorkMetadata
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
                        searching on

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


def fuzzy_search_quick_lookup(authors_quotes_works: List[AuthorQuoteWork], corpora_path: str,
                              num_processes: int, chunk_size: int,
                              quick_lookup_threshold: int) -> Tuple[Deque[QuoteMatch], Deque[int]]:
    '''
    Performs a fuzzy search over a given list of
    quick lookup authors, quotes, and works

    Args:
        authors_quotes_works:   The list of authors, quotes, and works to
                                use when searching
        corpora_path:           The path to the corpora home directory
        num_processes:          The number of processes to use for the search
        chunk_size:             The size of each quote chunk to perform
                                multiprocessed searching on
        quick_lookup_threshold: The threshold to use for passing or failing a
                                found match

    Returns:    A 2-tuple in which the first element a deque of the matches
                that passed the search and the second is a deque of the ids
                of the quotes that failed the search
    '''
    failed_quick_lookup_quote_ids: Deque[int] = deque()
    matches: Deque[QuoteMatch] = deque()
    for i, (author, quotes, work_metadatas) in enumerate(authors_quotes_works, 1):
        author_matches: List[QuoteMatch] = fuzzy_search_multiprocessed(
            quotes, work_metadatas, corpora_path, num_processes, chunk_size)

        # Need to check if any of the matches for each quote
        # passed the threshold, and mark the ones without any
        # passing matches as failed
        quote_id_to_passing_status: Dict[int, False] = {
            q.id: False for q in quotes
        }
        for m in author_matches:
            # If at least one of the matches passes the
            # threshold, then the quote passes
            passing: bool = quote_id_to_passing_status[m.quote_id]
            quote_id_to_passing_status[m.quote_id] = passing or m.score >= quick_lookup_threshold

        # Add quote ids of quotes that failed the quick lookup
        # to the failed quotes deque
        failed_quick_lookup_quote_ids.extend([
            q_id for q_id, passing
            in quote_id_to_passing_status.items()
            if not passing
        ])

        # Only add passing matches to the matches table
        matches.extend([
            match_ for match_
            in author_matches
            if quote_id_to_passing_status[match_.quote_id] == True]
        )
        logging.info(
            "Finished quick lookup for %s / %s authors (%s)", i,
            len(authors_quotes_works), author)

    return matches, failed_quick_lookup_quote_ids


def fuzzy_search_auto_quick_lookup(authors_quotes_works: List[AuthorQuoteWork], corpora_path: str,
                                   num_processes: int, chunk_size: int,
                                   quick_lookup_threshold: int) -> Tuple[Deque[QuoteMatch], Deque[int]]:
    '''
    Fuzzy search quotes whose quick lookup works have not been manually
    compiled

    Same arguments, return types, and raises as fuzzy_search_quick_lookup
    '''
    MAX_NUM_WORKS = 1000

    # Automatically add quotes with >= 1000 works to failure queue
    auto_fail_id_lists: List[int] = [
        [q.id for q in quotes]
        for _, quotes, works
        in authors_quotes_works
        if len(works) >= MAX_NUM_WORKS
    ]

    # 3-tuples that have less than the max num of quotes should be checked
    to_check: List[AuthorQuoteWork] = [
        AuthorQuoteWork(author, quotes, works)
        for author, quotes, works
        in authors_quotes_works
        if len(works) < MAX_NUM_WORKS
    ]

    matches, failed_quick_lookup_quote_ids = fuzzy_search_quick_lookup(
        to_check, corpora_path,
        num_processes, chunk_size,
        quick_lookup_threshold)

    # Could probably change list comprehension to avoid needing to loop,
    # but oh well
    for fail_id_list in auto_fail_id_lists:
        failed_quick_lookup_quote_ids.extend(fail_id_list)

    return matches, failed_quick_lookup_quote_ids
