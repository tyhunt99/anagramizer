import json
import pytest

from app import create_app


@pytest.fixture(scope='module')
def app():
    '''
    Represents the running application. Note that this is built at
    module scope, meaning it will collect state over time.

    There are other possbiel methods for doing this such as:
      - Using pytest.fixture(autouse=True), runs before each test
      - boiler plate code in all the places
    '''
    app = create_app()
    app.config.update({'TESTING': True})
    yield app


def test_adding_words(client):
    res = client.post(
        '/words.json',
        data=json.dumps({'words': ["read", "dear", "dare"]}),
    )
    assert res.status_code == 201


def test_fetching_anagrams(client):
    res = client.get('/anagrams/read.json')
    assert res.status_code == 200
    body = json.loads(res.data)
    assert len(body['anagrams']) > 0
    expected_anagrams = sorted(['dare', 'dear'])
    assert body['anagrams'] == expected_anagrams


def test_fetching_anagrams_with_limit(client):
    # initialize test data
    client.post(
        '/words.json',
        data=json.dumps({'words': ["read", "dear", "dare"]}),
    )
    res = client.get('/anagrams/read.json?limit=1')
    assert res.status_code == 200
    body = json.loads(res.data)
    assert len(body['anagrams']) > 0
    expected_anagrams = sorted(['dare'])
    assert body['anagrams'] == expected_anagrams

def test_fetch_for_word_with_no_anagrams(client):
    # fetch anagrams with limit
    res = client.get('/anagrams/zyxwv.json')
    assert res.status_code == 200
    body = json.loads(res.data)
    assert len(body['anagrams']) == 0

def test_deleting_all_words(client):
    client.post(
        '/words.json',
        data=json.dumps({'words': ["read", "dear", "dare"]}),
    )
    res = client.delete('/words.json')
    assert res.status_code == 204
    res = client.get('/anagrams/read.json')
    assert res.status_code == 200
    body = json.loads(res.data)
    assert len(body['anagrams']) == 0

def test_deleting_all_words_multiple_times(client):
    for _ in range(1, 3):
        res = client.delete('/words.json')
        assert res.status_code == 204
    # should fetch an empty body
    res = client.get('/anagrams/read.json')
    assert res.status_code == 200
    body = json.loads(res.data)
    assert len(body['anagrams']) == 0

def test_deleting_single_word(client):
    # initialize test data
    client.post(
        '/words.json',
        data=json.dumps({'words': ["read", "dear", "dare"]}),
    )
    res = client.delete('/words/dear.json')
    assert res.status_code == 204
    res = client.get('/anagrams/read.json')
    assert res.status_code == 200
    body = json.loads(res.data)
    expected_anagrams = sorted(['dare'])
    assert body['anagrams'] == expected_anagrams

def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    body = json.loads(res.data)
    assert 'stats' in body
    assert 'words' in body

def test_anagram_size_limit(client):
    client.post(
        '/words.json',
        data=json.dumps({'words': ["read", "dear", "dare"]}),
    )
    res = client.get('/anagrams/more/5')
    assert res.status_code == 200
    body = json.loads(res.data)
    assert len(body['anagrams']) == 0
    res = client.get('/anagrams/more/3')
    assert res.status_code == 200
    body = json.loads(res.data)
    assert len(body['anagrams']) == 1

def test_stats(client):
    client.post(
        '/words.json',
        data=json.dumps({'words': ["read", "dear", "dare"]}),
    )
    res = client.get('/anagrams/stats')
    assert res.status_code == 200
    expected_stats = {
        'latest': True,
        'max': 4,
        'mean': 4,
        'median': 4,
        'min': 4,
        'num_words': 3,
        'top_anagrams': []
    }
    body = json.loads(res.data)
    assert body == expected_stats
