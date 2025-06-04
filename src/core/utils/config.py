# -*- coding: utf-8 -*-

"""
Module: config
Author: creagleone
Date: 2025-05-07

Description:
    This module contains functions to manage technical tables

Dependencies:
    - sqlite3
    - datetime (datetime)
    - wraps (functools)
    - exceptions.py
    - common.py

Usage Example:
    N/A

Notes:
    - N/A
"""

import sqlite3
from datetime import datetime
from functools import wraps
from core.utils import exceptions, common


def _sqlite(f):
    """
    Manage connection to SQLite database for config

    Args:
        f (function): Function to perform

    Returns:
        sqlite3.Connection: Connection datas
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        db_path = common.get_work_files("database.db")
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            kwargs['conn'] = conn
            result = f(*args, **kwargs)
            conn.commit()
        except sqlite3.OperationalError as e:
            if conn:
                conn.rollback()
            if "database is locked" in str(e).lower():
                raise exceptions.Error(501, e)
            if "disk i/o error" in str(e).lower():
                raise exceptions.Error(503, e)
            if "out of memory" in str(e).lower():
                raise exceptions.Error(502, e)
            raise exceptions.Error(500, e)
        finally:
            if conn:
                conn.close()
        return result
    return wrapper


@_sqlite
def insert_query_db(query: str, args: tuple, **kwargs) -> int:
    """
    Insert a new database settings

    Args:
        query (str): Query to perform
        args (tuple): Query args

    Returns:
        int: Return code
    """
    try:
        conn = kwargs.get('conn')
        cursor = conn.cursor()
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        args = args + (formatted_datetime,)
        cursor.execute(query, args)
    except sqlite3.IntegrityError as e:
        raise exceptions.Error(402, e)
    except sqlite3.OperationalError as e:
        if "syntax error" in str(e).lower():
            raise exceptions.Error(403, e)
        if "no such table" in str(e).lower():
            raise exceptions.Error(404, e)
        raise exceptions.Error(401, e)
    return 200


@_sqlite
def update_settings(query, args: tuple, **kwargs):
    """
    Updates the language

    Args:
        query (str): Query to perform
        args (tuple): Query args
    """
    try:
        conn = kwargs.get('conn')
        cursor = conn.cursor()
        cursor.execute(query, args)
    except sqlite3.OperationalError as e:
        if "no such" in str(e).lower():
            raise exceptions.Error(404, e)
        if "syntax error" in str(e).lower():
            raise exceptions.Error(403, e)
        raise exceptions.Error(401, e)


@_sqlite
def get_settings(query, args: tuple, **kwargs):
    """
    Retrieves the language

    Args:
        query (str): Query to perform

    Returns:
        tuple: Query result
    """
    try:
        conn = kwargs.get('conn')
        cursor = conn.cursor()

        cursor.execute(query, args)
        return cursor.fetchone()[0]

    except sqlite3.OperationalError as e:
        if "no such" in str(e).lower():
            raise exceptions.Error(404, e)
        if "syntax error" in str(e).lower():
            raise exceptions.Error(403, e)
        raise exceptions.Error(401, e)


@_sqlite
def get_list_data(query, **kwargs) -> tuple:
    """
    Recover saved database settings

    Args:
        query (str): Query to perform

    Returns:
        tuple: Query result
    """
    try:
        conn = kwargs.get('conn')
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        if "no such" in str(e).lower():
            raise exceptions.Error(404, e)
        if "syntax error" in str(e).lower():
            raise exceptions.Error(403, e)
        raise exceptions.Error(401, e)


@_sqlite
def setup_db(**kwargs) -> int:
    """
    Prepare the app database

    Returns:
        int: Return code
    """
    conn = kwargs.get('conn')
    cursor = conn.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS db_config  (
            id                INTEGER      PRIMARY KEY ON CONFLICT ROLLBACK
                                        AUTOINCREMENT
                                        UNIQUE
                                        NOT NULL,
            connection_type    VARCHAR (20) NOT NULL,
            name              VARCHAR (60) UNIQUE ON CONFLICT ROLLBACK
                                        NOT NULL,
            settings          TEXT         NOT NULL
                                        DEFAULT ('{}'),
            created_at      DATETIME     NOT NULL,
            updated_at  DATETIME
        );"""
    cursor.execute(query)
    query = """
        CREATE TABLE IF NOT EXISTS settings (
            id       INTEGER PRIMARY KEY ON CONFLICT ROLLBACK AUTOINCREMENT
                            NOT NULL ON CONFLICT ROLLBACK,
            [key]            UNIQUE ON CONFLICT ROLLBACK
                            NOT NULL ON CONFLICT ROLLBACK,
            [values]         NOT NULL ON CONFLICT ROLLBACK,
            created_at      DATETIME     NOT NULL,
            updated_at  DATETIME
        );"""
    cursor.execute(query)
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    query = f"""
        INSERT INTO settings ([key], [values], created_at)
        VALUES ('locale', 'en_US', '{formatted_datetime}')
        ON CONFLICT([key]) DO NOTHING;
    """
    cursor.execute(query)
    return 200
