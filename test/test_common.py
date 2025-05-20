
from unittest.mock import patch, mock_open, MagicMock
import pytest
from src.core.utils import common


@patch('os.path.getsize')
def test_get_file_size(mock_getsize):
    mock_getsize.return_value = 1024
    file_size = common.get_file_size('fichier_fictif.txt')
    assert file_size == "1.00 Ko"

    mock_getsize.return_value = 1024 * 1024 * 1024
    file_size = common.get_file_size('fichier_fictif.txt')
    assert file_size == "1.00 Go"


def test_merge_common_keys():

    assert not common.merge_common_keys({}, {})

    dict1 = [('Table1', 'text', 4), ('Table2', 'texte', 5)]
    dict2 = [('Table2', 23, 'value'), ('Table3', 'result', 5)]

    merged_dict = common.merge_common_keys(dict1, dict2)
    assert merged_dict == {'Table2': ['texte', 23, 5, 'value']}


@patch('hashlib.new')
@patch('gzip.open', new_callable=mock_open, read_data=b'some data')
@patch('builtins.open', new_callable=mock_open, read_data=b'some data')
def test_get_hash_file(mock_file, mock_gz_open, mock_hashlib):
    mock_hasher = MagicMock()
    mock_hasher.hexdigest.return_value = 'mocked_hash'
    mock_hashlib.return_value = mock_hasher

    file_path = 'fichier.txt'
    assert common.get_hash_file(file_path) == 'mocked_hash'
    mock_file.assert_called_once_with(file_path, 'rb')

    gz_file_path = 'fichier.gz'
    assert common.get_hash_file(gz_file_path) == 'mocked_hash'
    mock_gz_open.assert_called_once_with(gz_file_path, 'rb')


@patch('hashlib.new')
@patch('gzip.open', new_callable=mock_open, read_data=b'some data')
@patch('builtins.open', new_callable=mock_open, read_data=b'some data')
def test_get_hash_file_with_another_algo(mock_file, mock_gz_open,
                                         mock_hashlib):
    mock_hasher = MagicMock()
    mock_hasher.hexdigest.return_value = 'mocked_hash_different_algorithm'
    mock_hashlib.return_value = mock_hasher

    file_path = 'fichier.txt'
    assert common.get_hash_file(
        file_path, 'md5') == 'mocked_hash_different_algorithm'
    mock_file.assert_called_once_with(file_path, 'rb')

    gz_file_path = 'fichier.gz'
    assert common.get_hash_file(
        gz_file_path, 'md5') == 'mocked_hash_different_algorithm'
    mock_gz_open.assert_called_once_with(gz_file_path, 'rb')


@pytest.mark.parametrize("s1, s2, expected", [
    ("kitten", "sitting", 3),
    ("flaw", "lawn", 2),
    ("", "", 0),
    ("abc", "", 3),
    ("", "abc", 3),
    ("hello", "hello", 0),
    ("abc", "def", 3),
    ("abcdef", "abc", 3),
])
def test_levenshtein_distance(s1, s2, expected):
    assert common.levenshtein_distance(s1, s2) == expected


@pytest.mark.parametrize("pairs, expected", [
    ([("a,b,c", "b,c,d")], [(("a,b,c", "b,c,d"), {"a", "d"})]),
    ([("x,y,z", "x,y")], [(("x,y,z", "x,y"), {"z"})]),
    ([("1,2,3", "2,3,4")], [(("1,2,3", "2,3,4"), {"1", "4"})]),
    ([("", "")], [(("", ""), set())]),
    ([("same,same", "same,same")], [(("same,same", "same,same"), set())]),
])
def test_compare_pairs(pairs, expected):
    assert common.compare_pairs(pairs) == expected
