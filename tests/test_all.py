import gzip
import os
import pytest

from anagramizer import Anagramizer


@pytest.fixture
def initial_expected_structure():
    return {
        'aadm': set(['Adam']),
        'ader': set(['dear', 'read']),
        'aelpp': set(['apple']),
        'amt': set(['Mat', 'mat']),
        'art': set(['rat', 'tar', 'art']),
    }


def test_initialization(initial_expected_structure):
    a = Anagramizer('tests/data/test_initialization.txt')
    assert a._words == initial_expected_structure


def test_gzip_initialization(initial_expected_structure):
    a = Anagramizer('tests/data/test_initialization.txt.gz')
    assert a._words == initial_expected_structure


def test_empty_initialization(initial_expected_structure):
    a = Anagramizer('')
    assert a._words == {}


def test_save_to_file():
    a = Anagramizer('tests/data/test_initialization.txt')
    save_file = 'tests/data/tmp_test_save_to_file.txt'
    expected = 'Adam\nMat\napple\nart\ndear\nmat\nrat\nread\ntar'
    a._save_to_file(save_file)
    with open(save_file) as f:
        save_content = f.read()
    assert save_content == expected
    os.unlink(save_file)


def test_save_to_file_cpmpressed():
    a = Anagramizer('tests/data/test_initialization.txt')
    save_file = 'tests/data/tmp_test_save_to_file.gz'
    expected = 'Adam\nMat\napple\nart\ndear\nmat\nrat\nread\ntar'
    a._save_to_file(save_file, True)
    with gzip.open(save_file, 'rb') as f:
        save_content = f.read().decode()
    assert save_content == expected
    os.unlink(save_file)


def test_add_existing_word_to_dict(initial_expected_structure):
    a = Anagramizer('tests/data/test_initialization.txt')
    assert a.add_word('dear')
    assert a._words == initial_expected_structure


def test_add_new_word_to_dict():
    a = Anagramizer()
    expected = {
        'ader': set(['dear']),
    }
    assert a.add_word('dear')
    assert a._words == expected


def test_remove_word_from_dict():
    a = Anagramizer()
    expected = {
        'ader': set([]),
    }
    assert not a.remove_word('tar')
    a.add_word('dear')  # testedby another test?
    assert a.remove_word('dear')
    assert a._words == expected


def test_remove_anagrams():
    a = Anagramizer('tests/data/test_initialization.txt')
    expected = {
        'aadm': set(['Adam']),
        'aelpp': set(['apple']),
        'amt': set(['Mat', 'mat']),
        'art': set(['rat', 'tar', 'art']),
    }
    assert a.remove_anagrams('read')
    assert not a.remove_anagrams('xyzzz')
    assert a._words == expected


def test_remove_all_words():
    a = Anagramizer('tests/data/test_initialization.txt')
    assert len(a._words) > 0
    a.remove_all()
    assert len(a._words) == 0


def test_word_list():
    a = Anagramizer('tests/data/test_initialization.txt')
    expected = [
        'Adam',
        'Mat',
        'apple',
        'art',
        'dear',
        'mat',
        'rat',
        'read',
        'tar'
    ]
    assert a.word_list() == expected

@pytest.mark.parametrize(
    'word, expected', [
        ('read', True),
        ('xzzy', False),
    ])
def test_word_exists(word, expected):
    a = Anagramizer('tests/data/test_initialization.txt')
    assert a._word_exists(word) == expected


@pytest.mark.parametrize(
    'word, limit, include_proper, expected_list', [
        ('tar', -1, False, ['art', 'rat']),
        ('rat', -1, False, ['art', 'tar']),
        ('rat', 1, False, ['art']),
        ('rat', 0, False, []),
        ('mat', -1, False, []),
        ('mat', -1, True, ['Mat']),
        ('banana', -1, False, []),
    ])
def test_getting_anagrams(word, limit, include_proper, expected_list):
    a = Anagramizer('tests/data/test_initialization.txt')
    assert a.get_anagrams(word, limit, include_proper) == expected_list


@pytest.mark.parametrize(
    'words, expected', [
        ([], False),
        (['tar', 'rat'], True),
        (['tar', 'rat', 'ball'], False),
    ])
def test_are_anagrams(words, expected):
    a = Anagramizer()
    assert a.are_anagrams(words) == expected
