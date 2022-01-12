# pylint: disable=redefined-outer-name
import json
from pytest import fixture

from tests import common
import meilisearch
from meilisearch.errors import MeiliSearchApiError

@fixture(scope='session')
def client():
    return meilisearch.Client(common.BASE_URL, common.MASTER_KEY)

@fixture(autouse=True)
def clear_indexes(client):
    """
    Auto-clears the indexes after each test function run.
    Makes all the test functions independent.
    """
    # Yields back to the test function.
    yield
    # Deletes all the indexes in the MeiliSearch instance.
    indexes = client.get_indexes()
    for index in indexes:
        task = client.index(index.uid).delete()
        client.wait_for_task(task['uid'])

@fixture(scope='function')
def indexes_sample(client):
    indexes = []
    for index_args in common.INDEX_FIXTURE:
        task = client.create_index(**index_args)
        client.wait_for_task(task['uid'])
        indexes.append(client.get_index(index_args['uid']))
    # Yields the indexes to the test to make them accessible.
    yield indexes

@fixture(scope='session')
def small_movies():
    """
    Runs once per session. Provides the content of small_movies.json.
    """
    with open('./datasets/small_movies.json', 'r', encoding='utf-8') as movie_file:
        yield json.loads(movie_file.read())

@fixture(scope='session')
def small_movies_json_file():
    """
    Runs once per session. Provides the content of small_movies.json from read.
    """
    with open('./datasets/small_movies.json', 'r', encoding='utf-8') as movie_json_file:
        return movie_json_file.read().encode('utf-8')

@fixture(scope='session')
def songs_csv():
    """
    Runs once per session. Provides the content of songs.csv from read..
    """
    with open('./datasets/songs.csv', 'r', encoding='utf-8') as song_csv_file:
        return song_csv_file.read().encode('utf-8')

@fixture(scope='session')
def songs_ndjson():
    """
    Runs once per session. Provides the content of songs.ndjson from read..
    """
    with open('./datasets/songs.ndjson', 'r', encoding='utf-8') as song_ndjson_file:
        return song_ndjson_file.read().encode('utf-8')

@fixture(scope='function')
def empty_index(client):
    def index_maker(index_name=common.INDEX_UID):
        task = client.create_index(uid=index_name)
        client.wait_for_task(task['uid'])
        return client.get_index(uid=index_name)
    return index_maker

@fixture(scope='function')
def index_with_documents(empty_index, small_movies):
    def index_maker(index_name=common.INDEX_UID, documents=small_movies):
        index = empty_index(index_name)
        task = index.add_documents(documents)
        index.wait_for_task(task['uid'])
        return index
    return index_maker

@fixture(scope='function')
def test_key(client):
    key_info = {'description': 'test', 'actions': ['search'], 'indexes': ['movies'], 'expiresAt': None}

    key = client.create_key(key_info)

    yield key

    try:
        client.delete_key(key['key'])
    except MeiliSearchApiError:
        pass


@fixture(scope='function')
def test_key_info(client):
    key_info = {'description': 'test', 'actions': ['search'], 'indexes': [common.INDEX_UID], 'expiresAt': None}

    yield key_info

    try:
        keys = client.get_keys()['results']
        key = next(x for x in keys if x['description'] == key_info['description'])
        client.delete_key(key['key'])
    except MeiliSearchApiError:
        pass
