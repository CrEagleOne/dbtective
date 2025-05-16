# -*- coding: utf-8 -*-

"""
Module: orders
Auteur: creagleone
Date: 2025-05-07
Description:
    This module contains functions to execute database comparaison

Dependencies:
    - pandas
    - common.py
    - exceptions.py
    - logs.py
    - duck.py
    - settings.py

Usage Example:
    - N/A

Notes:
    - N/A
"""

import pandas
from core.utils import common, exceptions, logs
from core.database import duck
from gui.core import settings


def compare_db(mode: str, settings_db1: list, settings_db2: list,
               segment: int | None, fetch: int) -> int:
    """
    Execute database comparaison

    Args:
        mode (str): Type of processing to perform
        settings_db1 (list): Database connection parameters
        settings_db2 (list): Database connection parameters
        segment (int | None): Segment size
        fetch (int): Fetch size

    Raises:
        exceptions.Warn: code 300 (data gap)

    Returns:
        int: code 201 (No data gap)
    """
    settings_data = settings.Settings().get_settings()
    master_name = settings_data["workconfig"]["files"][0]
    slave_name = settings_data["workconfig"]["files"][1]
    extension = settings_data["workconfig"]["extension"]

    warn = False

    tables = common.get_common_tables(
        settings_db1, settings_db2)

    for table in tables:
        common.extract_to_csv(
            settings_db1[1], table, master_name + extension, segment, fetch)

        common.extract_to_csv(
            settings_db2[1], table, slave_name + extension, segment, fetch)

        if mode == "hash":
            hash1 = common.get_hash_file(master_name + extension)
            hash2 = common.get_hash_file(master_name + extension)
            if hash1 != hash2:
                warn = True
                logs.log_warn(f"Gap found for table {table}")

        elif mode == "full":
            duck.load_file_data(
                filename=master_name + extension, tablename=master_name)
            duck.load_file_data(
                filename=slave_name + extension, tablename=slave_name)

            query = f'''SELECT * FROM {master_name} EXCEPT
                SELECT * FROM {slave_name}'''
            data = duck.get_datas_by_fetchdf(query)

            if isinstance(data, pandas.DataFrame):
                if not data.empty:
                    outfile = f"gap_{table}.csv"
                    common.create_gap_files(outfile, data)

    if mode != "hash":
        duck.delete_tmp_db()

    if warn:
        raise exceptions.Warn(300)

    return 201
