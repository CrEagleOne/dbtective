# -*- coding: utf-8 -*-

"""
Module: duckdb
Auteur: creagleone
Date: 2025-05-07
Description:
    This module contains the functions to load and process comparison data

Dépendances:
    - os
    - wraps (functools)
    - duckdb
    - pandas
    - settings.py
    - common.py

Usage Example:
    N/A

Notes:
    - This module uses DuckDB for efficient in-memory SQL processing.
    - Designed for handling large datasets efficiently.
"""

import os
from functools import wraps
import duckdb
import pandas
from gui.core import settings
from core.utils import common


def _duckdb(f):
    """
    Manage connection to SQLite database

    Args:
        f (function): Function to perform

    Returns:
        duckdbDuckDBPyConnection: Connection datas
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        Database access

        Raises:
            gerer_retour: Error(Erreurs duckDB)

        Returns:
            duckdbDuckDBPyConnection: Connection datas
        """
        try:
            tmp_db = settings.Settings().get_settings()["workconfig"]["db"]
            db_path = common.get_work_files(tmp_db)
            cnn = duckdb.connect(database=db_path)
            kwargs['cnn'] = cnn
            rv = f(*args, **kwargs)

        except duckdb.Error as e:
            print(e)
        finally:
            cnn.close()
        return rv
    return wrapper


@_duckdb
def retrieve_file_delimiter(filename: str, **kwargs) -> str:
    """
    Retrieves the CSV delimiter from the file

    Args:
        filename (str): Filename

    Returns:
        str: Delimiter
    """
    cnn = kwargs.get('cnn')
    req = f"SELECT delimiter FROM sniff_csv('{filename}')"
    try:
        result = cnn.execute(req).fetchone()[0]
    except (duckdb.CatalogException, duckdb.ParserException,
            duckdb.BinderException) as e:
        print(e)
    return result


@_duckdb
def load_file_data(filename: str, tablename: str, **kwargs) -> bool:
    """
    Load the contents of a file into the database

    Args:
        filename (str): Filename
        tablename (str): Name of the table

    Returns:
        bool: True if successful, False otherwise
    """
    cnn = kwargs.get('cnn')
    delimiter = retrieve_file_delimiter(filename=filename)
    try:
        cnn.execute(f"""
            CREATE OR REPLACE TABLE {tablename} AS
            SELECT * FROM read_csv('{filename}', delim='{delimiter}',
            all_varchar=True, header=True, store_rejects=True,
            rejects_scan='rejects_scan', rejects_table='rejects_table')
        """)
    except (duckdb.IOException, duckdb.CatalogException,
            duckdb.ConstraintException, duckdb.TransactionException,
            duckdb.ParserException, duckdb.BinderException,
            duckdb.InvalidTypeException, duckdb.OutOfMemoryException,
            duckdb.InvalidInputException, duckdb.ConversionException,
            duckdb.SerializationException) as e:
        print(e)
    return True


@_duckdb
def get_datas_by_fetchdf(query: str, arg: tuple = None,
                         **kwargs) -> pandas.DataFrame:
    """
    Retrieves all rows as a data frame

    Args:
        query (str): SQL query
        arg (optional, Tuple): Query args

    Returns:
        pd.DataFrame: Query result
    """
    cnn = kwargs.get('cnn')
    try:
        result = cnn.execute(query, arg).fetchdf()
    except (duckdb.CatalogException, duckdb.ParserException,
            duckdb.BinderException) as e:
        print(e)

    return result


def delete_tmp_db():
    """
    Delete tmp duckDB database
    """
    tmp_db = settings.Settings().get_settings()["workconfig"]["db"]
    db_path = common.get_work_files(tmp_db)
    os.remove(db_path)
