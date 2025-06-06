
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

    dict1 = (
        ('key1', 100, 200, 300),
        ('key2', 150, 250, 350),
        ('key3', 400, 500, 600)
    )

    dict2 = (
        ('key1', 120, 220, 320),
        ('key2', 170, 270, 370),
        ('key4', 450, 550, 650)
    )

    result = common.merge_common_keys(dict1, dict2)

    expected_result = {
        'key1': ['20 octets', 20, 20],
        'key2': ['20 octets', 20, 20]
    }

    assert result == expected_result


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


@pytest.mark.parametrize("pairs, expected_result", [
    (
        [(",apple,banana,cherry", ",banana,cherry,date")],
        [((",apple,banana,cherry", ",banana,cherry,date"), {'apple', 'date'})]
    ),
    (
        [(",apple,banana", ",cherry,date")],
        [((",apple,banana", ",cherry,date"), {
          'apple', 'banana', 'cherry', 'date'})]
    ),
    (
        [(",apple,banana,cherry,date", ",apple,banana,cherry,date")],
        [((",apple,banana,cherry,date", ",apple,banana,cherry,date"), set())]
    ),
    (
        [(",apple", ",banana")],
        [((",apple", ",banana"), {'apple', 'banana'})]
    ),
    (
        [(",a,b,c", ",b,c,d"), (",e,f", ",f,g")],
        [
            ((",a,b,c", ",b,c,d"), {'a', 'd'}),
            ((",e,f", ",f,g"), {'e', 'g'})
        ]
    )
])
def test_compare_pairs(pairs, expected_result):
    assert common.compare_pairs(pairs) == expected_result


def test_get_suitable_unit_for_size():
    assert common.get_suitable_unit_for_size(100) == "100 octets"
    assert common.get_suitable_unit_for_size(1500) == "1.46 Ko"
    assert common.get_suitable_unit_for_size(1500000) == "1.43 Mo"
    assert common.get_suitable_unit_for_size(1500000000) == "1.40 Go"
    assert common.get_suitable_unit_for_size(1023) == "1023 octets"
    assert common.get_suitable_unit_for_size(1024) == "1.00 Ko"
    assert common.get_suitable_unit_for_size(1024**2) == "1.00 Mo"
    assert common.get_suitable_unit_for_size(1024**3) == "1.00 Go"
