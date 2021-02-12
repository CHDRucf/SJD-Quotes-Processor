import json
import operator
import os
import re
import string
import typing
from itertools import chain
from typing import Dict, Iterable, Iterator, List, Set, Tuple, Union

import dotenv
import Levenshtein
import sshtunnel
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import CursorBase

QuoteDict = typing.NewType("QuoteDict", Dict[str, Union[str, int]])

HeadwordQuotesDict = typing.NewType(
    "HeadwordQuotesDict", Dict[str, List[QuoteDict]])

FlattenedQuotesDict = typing.NewType(
    "FlattenedQuotesDict", List[Dict[str, Union[str, int]]])

Metadata = typing.NewType("Metadata", Dict[str, str])

MatchToMetadataDict = typing.NewType("MetadataDict", Dict[str, Metadata])


def split_by_punctuation() -> List[str]:
    '''
    TODO
    '''
    ...


def get_file_paths(top: str) -> Iterator[str]:
    '''
    Recursively finds all the filepaths starting from the specified
    directory.
    TODO: Filter the results so that only .txt files are returned?

    Args:
        top:    The directory to start searching from

    Returns:    An iterator with all the filepaths found
    '''
    return chain.from_iterable([file_names for _, _, file_names in os.walk(top)])


def get_ssh_connection_options_from_env() -> Dict[str, Union[str, int]]:
    '''
    Loads the SSH connection options from the current environment
    into a dictionary suitable for being passed into the
    ssh.SSHTunnelForwarder method (ideally used as a context manager
    with the "with" keyword)

    Raises: EnvironmentError if any of the connection options are not found
    '''
    required_env_vars: List[str] = ["SSH_HOST", "SSH_PORT", "SSH_USER", "SSH_PASS",
                                    "_REMOTE_BIND_ADDRESS", "_REMOTE_MYSQL_PORT"]

    for var in required_env_vars:
        val = os.getenv(var)
        if not val:
            raise EnvironmentError(f"Environment variable {var} not set")

    return {
        "ssh_address_or_host": (os.getenv("SSH_HOST"), int(os.getenv("SSH_PORT"))),
        "ssh_username": os.getenv("SSH_USER"),
        "ssh_password": os.getenv("SSH_PASS"),
        "remote_bind_address": (os.getenv("_REMOTE_BIND_ADDRESS"), int(os.getenv("_REMOTE_MYSQL_PORT"))),
    }


def get_database_connection_options_from_env(get_port: bool = False) -> Dict[str, str]:
    '''
    Loads the database connection options from the current environment
    into a dictionary suitable for being passed into the
    mysql.connector.connect method.

    Args:
        get_port:   Whether or not to read the database port number from the
                    environment. This should be false if accessing the database
                    via an SSH tunnel

    Raises: EnvironmentError if any of the connection options are not found
    '''
    opt_env_var: Dict[str, str] = {
        "user": "DB_USER",
        "password": "DB_PASS",
        "host": "DB_HOST",
        "database": "DB_DB",
    }
    if get_port:
        opt_env_var["port"] = "DB_PORT"

    result: Dict[str, str] = {
        opt: os.getenv(env_var)
        for opt, env_var in opt_env_var.items()
    }

    for key, val in result.items():
        if not val:
            raise EnvironmentError(
                f"Environment variable {opt_env_var[key]} not set")
    return result


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


def write_to_database(quote: QuoteDict, top_five: Dict[str, float], conn: MySQLConnection) -> None:
    '''
    Args:
        quote:      An dictionary containing all the necessary fields for
                    writing the quote to the quotes table
        top_five:   A dictionary containing the top five matches for the given
                    quote mapped to their metadata
        conn:       The MySQLConnection object representing a connection to the
                    database

    TODO: Test this. The method for obtaining the correct id for a quote may not work
    '''
    sql_query_quote_id = ("SELECT id "
                          "FROM quotes "
                          "WHERE quote = %s AND author = %s AND headword = %s;")
    sql_insert_statement = ("INSERT INTO matches(quote_id, metadata_id, rank, score, content)"
                            "VALUES (%s, %s, %s, %s, %s);"
                            )
    cursor: CursorBase = conn.cursor()
    for sentence, metadata in top_five:
        cursor.execute(sql_query_quote_id, (quote.quote,
                                            quote.author, quote.headword))
        quote_id_row: Tuple[int] = cursor.fetchone()
        cursor.execute(sql_insert_statement,
                       (quote_id_row[0], metadata.get("id"), 0, metadata.get("score"), sentence))
        conn.commit()


def get_file_metadata(file_name: str, cursor: CursorBase) -> Metadata:
    '''
    Returns a dict containing the metadata for a written work with
    the given file name

    Args:
        file_name:  The name of the file to obtain the metadata for
        cursor:     The database cursor for performing the metadata query
    # TODO: Test

    Returns:    A dictionary representing the SQL record for the given file's
                metadata
    '''
    sql_query: str = (
        "SELECT id, title, author, url, filepath, lccn "
        "FROM METADATA "
        "WHERE filepath = %s;")

    cursor.execute(sql_query, (file_name,))

    id_, title, author, url, filepath, lccn = cursor.fetchone()
    return {
        "id": id_,
        "title": title,
        "author": author,
        "url": url,
        "filepath": filepath,
        "lccn": lccn
    }


def jaccard_index(set1: set, set2: set) -> float:
    ''' Computes the Jaccard Index between two sets'''
    return len(set1 & set2) / len(set1 | set2)


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


def main() -> None:
    # TODO: Turn these constants into command line args using begins package
    # TODO: Log errors using the logger module instead
    #       of printing them to the console
    # TODO: Try to make this main function smaller
    # TODO: Add a config so that dotenv only loads in development, not in
    #       final product
    JSON_FILEPATH = "./quotes.json"
    CORPORA_PATH = "."

    dotenv.load_dotenv()

    try:
        ssh_connection_options: Dict[str, Union[str, int]
                                     ] = get_ssh_connection_options_from_env()
    except EnvironmentError as e:
        print(e)
        return

    try:
        database_connection_options: Dict[str,
                                          str] = get_database_connection_options_from_env()
    except EnvironmentError as e:
        print(e)
        return

    conn: MySQLConnection
    cursor: CursorBase
    try:
        with sshtunnel.SSHTunnelForwarder(**ssh_connection_options) as tunnel:
            conn = connect(**database_connection_options,
                           port=tunnel.local_bind_port)
            cursor = conn.cursor()

        # Refer to convert-excel-to-json module for quote object schema
        headword_quotes: HeadwordQuotesDict
        try:
            with open(JSON_FILEPATH, "r") as fp:
                headword_quotes = json.load(fp)
        except FileNotFoundError as fnfe:
            print(fnfe)
            return

        # Get the list of quote objects, with the headword added to each object
        quotes: FlattenedQuotesDict = flatten_quotes(headword_quotes)

        # Convert to list to avoid exhausting iterator
        file_paths: List[str] = list(get_file_paths(CORPORA_PATH))

        for quote in quotes:
            top_five: MatchToMetadataDict = fuzzy_search_over_corpora(
                quote.get("quote"), file_paths, cursor)
            write_to_database(quote, top_five, cursor)

        cursor.close()
        conn.close()

    except Exception as e:
        print("Unable to connect to the database due to the following error:")
        print(e)
        print("Please ensure that the correct environment variables are set and that you are connected to the VPN")
        return
