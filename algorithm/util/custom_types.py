'''custom_types.py

Contains type aliases for verbose types used by the fuzzy search algorithm
and its auxiliary functions
'''

from typing import Dict, List, NewType, Union

QuoteDict = NewType("QuoteDict", Dict[str, Union[str, int]])

HeadwordQuotesDict = NewType(
    "HeadwordQuotesDict", Dict[str, List[QuoteDict]])

FlattenedQuotesDict = NewType(
    "FlattenedQuotesDict", List[Dict[str, Union[str, int]]])

Metadata = NewType("Metadata", Dict[str, str])

MatchToMetadataDict = NewType("MetadataDict", Dict[str, Metadata])
