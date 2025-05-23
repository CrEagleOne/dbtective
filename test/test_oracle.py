from unittest.mock import patch, MagicMock
import pytest
from src.core.database.oracle import (get_unique_data,
                                      get_list_data,
                                      get_data_by_segment)

db_config = {
    'username': 'user',
    'password': 'pass',
    'host': 'localhost',
    'port': '1521',
    'dsn': 'ORCL',
    'dsn_type': False
}

db_config_2 = {
    'username': 'user',
    'password': 'pass',
    'host': 'localhost',
    'port': '1521',
    'dsn': 'FREE',
    'dsn_type': True
}


@patch('src.core.database.oracle.oracledb')
def test_get_unique_data(mock_oracledb):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_oracledb.connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ('result',)
    result = get_unique_data(db_config, "SELECT * FROM table")
    assert result == ('result',)
    mock_cursor.execute.assert_called_once_with("SELECT * FROM table")
    mock_cursor.close.assert_called_once()


@patch('src.core.database.oracle.oracledb')
def test_get_unique_data_exception(mock_oracledb):
    mock_oracledb.connect.side_effect = Exception("Database error")

    with pytest.raises(Exception):
        get_unique_data(db_config, "SELECT * FROM table")


@patch('src.core.database.oracle.oracledb')
def test_get_list_data(mock_oracledb):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_oracledb.connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('TABLE1', 100, 5, 5000),
        ('TABLE2', 200, 6, 6000)
    ]

    query = """
        SELECT
            ut.TABLE_NAME,
            ut.NUM_ROWS AS "Nombre de lignes",
            COUNT(utc.COLUMN_NAME) AS "Nombre de colonnes",
            ut.BLOCKS * ut.AVG_ROW_LEN AS "Taille estimée (octets)"
        FROM USER_TABLES ut
        LEFT JOIN USER_TAB_COLUMNS utc ON ut.TABLE_NAME = utc.TABLE_NAME
        GROUP BY ut.TABLE_NAME, ut.NUM_ROWS, ut.BLOCKS, ut.AVG_ROW_LEN
    """

    result = get_list_data(db_config, query)
    assert result == [
        ('TABLE1', 100, 5, 5000),
        ('TABLE2', 200, 6, 6000)
    ]
    mock_cursor.execute.assert_called_once_with(query)
    mock_cursor.close.assert_called_once()


@patch('src.core.database.oracle.oracledb')
def test_get_list_data_exception(mock_oracledb):
    mock_oracledb.connect.side_effect = Exception("Database error")

    query = """
        SELECT
            ut.TABLE_NAME,
            ut.NUM_ROWS AS "Nombre de lignes",
            COUNT(utc.COLUMN_NAME) AS "Nombre de colonnes",
            ut.BLOCKS * ut.AVG_ROW_LEN AS "Taille estimée (octets)"
        FROM USER_TABLES ut
        LEFT JOIN USER_TAB_COLUMNS utc ON ut.TABLE_NAME = utc.TABLE_NAME
        GROUP BY ut.TABLE_NAME, ut.NUM_ROWS, ut.BLOCKS, ut.AVG_ROW_LEN
    """

    with pytest.raises(Exception):
        get_list_data(db_config, query)


@patch('src.core.database.oracle.oracledb')
def test_get_data_by_segment(mock_oracledb):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_oracledb.connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchmany.side_effect = [
        [('row1',), ('row2',)],
        [('row3',)],
        []
    ]

    mock_cursor.description = [("column1",), ("column2",)]

    mock_cursor.execute.side_effect = lambda query: None

    query = "SELECT * FROM table"

    expected_results = [
        [["column1", "column2"]],  # Column names first
        [('row1',), ('row2',)],
        [('row3',)]
    ]

    results = list(get_data_by_segment(db_config_2, segment_size=2, fetch=1,
                                       query=query, conn=mock_conn))

    assert results == expected_results

    assert mock_cursor.fetchmany.call_count == 3

    mock_cursor.close.assert_called_once()


@patch('src.core.database.oracle.oracledb')
def test_get_data_by_segment_exception(mock_oracledb):
    mock_oracledb.connect.side_effect = Exception("Database error")

    query = "SELECT * FROM table"

    with pytest.raises(Exception):
        list(get_data_by_segment(db_config_2, segment_size=2, fetch=1,
                                 query=query))
