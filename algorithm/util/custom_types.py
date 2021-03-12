'''custom_types.py

Contains NamedTuple types used by the fuzzy search algorithm

These types greatly simplify the algorithm, but keep in mind that they are
strongly coupled to the database schema
'''

from typing import List, NamedTuple, NewType, Tuple


class Quote(NamedTuple):
    id: int
    content: str


class WorkMetadata(NamedTuple):
    id: int
    title: str
    author: str
    url: str
    filepath: str
    lccn: str


class QuoteMatch(NamedTuple):
    '''
    ID field omitted since this program is the one writing the matches to the
    database, and the id of match records is auto-incrementing
    '''
    quote_id: int
    metadata_id: int
    rank: int
    score: float
    content: str


class AuthorQuoteWork(NamedTuple):
    author: str
    quotes: List[Quote]
    works: List[WorkMetadata]
