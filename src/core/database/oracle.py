# -*- coding: utf-8 -*-

"""
Module: oracle
Auteur: creagleone
Date: 2025-05-07
Description:
    This module contains the functions allowing you to retrieve data
    from an oracle database

Dépendances:
    - socket
    - wraps (functools)
    - oracledb
    - exceptions.py

Usage Example:
    N/A

Notes:
    - This module uses oracledb thin mode
    - Designed for handling large datasets efficiently.
"""

import socket
from functools import wraps
import oracledb
from core.utils import exceptions

oracledb.defaults.thin_mode = True


def _oracle(f):
    """
    Manage connection to Oracle database

    Args:
        f (function): Function to perform

    Returns:
        duckdbDuckDBPyConnection: Connection datas
    """
    @wraps(f)
    def wrapper(db_config, *args, **kwargs):
        try:
            username = db_config.get('username')
            password = db_config.get('password')
            host = db_config.get('host')
            port = db_config.get('port')

            dsn = f"{host}:{port}/{db_config.get('dsn')}" if \
                db_config.get('dsn_type') else \
                f"""(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))
                (CONNECT_DATA=(SERVICE_NAME={db_config.get('dsn')})))"""

            conn = oracledb.connect(user=username, password=password, dsn=dsn)
            kwargs['conn'] = conn
            return f(db_config, *args, **kwargs)
        except oracledb.DatabaseError as e:
            error = e.args[0]
            if error.code == 12541:
                raise exceptions.Error(504, error.message)
            if error.code == 28000:
                raise exceptions.Error(505, error.message)
            if error.code == 1017:
                raise exceptions.Error(506, error.message)

            raise exceptions.Error(500, error.message)
        except (oracledb.Error, socket.gaierror) as e:
            raise exceptions.Error(500, e)

    return wrapper


@_oracle
def get_unique_data(_db_config: list, query: str, **kwargs) -> tuple:
    """
    Retrieve the first result of a query

    Args:
        db_config (list): Database connection
        query (str): Query to perform

    Raises:
        exceptions.Error: list of error codes

    Returns:
        tuple: Query result
    """
    try:
        conn = kwargs.get('conn')
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone()
    except oracledb.DatabaseError as e:
        error = e.args[0]
        if error.code in [942, 904]:
            raise exceptions.Error(404, error.message)
        if error.code == 933:
            raise exceptions.Error(403, error.message)
        raise exceptions.Error(400, error.message)
    except oracledb.Error as e:
        raise exceptions.Error(401, e)
    finally:
        cursor.close()


@_oracle
def get_list_data(_db_config, query, **kwargs) -> tuple:
    """
    Retrieve all datas from a query

    Args:
        db_config (list): Database connection
        query (str): Query to perform

    Raises:
        exceptions.Error: list of error codes

    Returns:
        tuple: Query result
    """
    try:
        conn = kwargs.get('conn')
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except oracledb.DatabaseError as e:
        error = e.args[0]
        if error.code in [942, 904]:
            raise exceptions.Error(404, error.message)
        if error.code == 933:
            raise exceptions.Error(403, error.message)
        raise exceptions.Error(400, error.message)
    except oracledb.Error as e:
        raise exceptions.Error(401, e)
    finally:
        cursor.close()


@_oracle
def get_data_by_segment(_db_config, segment_size: int,
                        fetch: int, query, **kwargs):
    """
    Retrieve all datas from a query using segment and fetch

    Args:
        db_config (list): Database connection
        segment_size (int | None): How many rows are read per segment
        fetch (int): Number of rows to fetch per reading
        query (str): Query to perform

    Raises:
        exceptions.Error: code 100

    Yields:
        list: Segment data
    """
    try:
        conn = kwargs.get('conn')
        cursor = conn.cursor()
        total_row_count = 0
        current_offset = 0

        cursor.execute(f"{query} WHERE 1=0")
        column_names = [desc[0] for desc in cursor.description]
        yield [column_names]

        while True:
            if segment_size is None:
                paginated_query = query
            else:
                paginated_query = f"""{query} OFFSET {current_offset}
                    ROWS FETCH NEXT {segment_size} ROWS ONLY"""
            cursor.execute(paginated_query)

            current_segment = []
            total_row_count = 0
            while True:
                rows = cursor.fetchmany(fetch)
                if not rows:
                    if current_segment:
                        yield current_segment
                        current_segment = []
                    break
                current_segment.extend(rows)
                total_row_count += len(rows)

                if segment_size is None or \
                        len(current_segment) >= segment_size:
                    yield current_segment
                    break

            if not current_segment:
                break

            if segment_size is not None:
                current_offset += segment_size

        if current_segment:
            yield current_segment

    except oracledb.Error as e:
        raise exceptions.Error(100, e)
    finally:
        cursor.close()


@_oracle
def is_still_active(_db_config, **kwargs):
    """
    Checks if the database connection is still active

    Args:
        _db_config (Any): Database configuration
            (unused but included for compatibility)
        **kwargs (Any): Additional arguments, expecting a 'conn' key

    Returns:
        bool: True if the connection is active, False otherwise
    """
    conn = kwargs.get('conn')
    return conn.ping() is None
