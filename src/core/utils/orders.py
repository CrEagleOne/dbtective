# -*- coding: utf-8 -*-

"""
Module: orders
Auteur: creagleone
Date: 2025-05-07

Description:
    This module contains functions to execute database comparaison

Dependencies:
    - os
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

import os
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

    folder = common.get_work_folder("extracts")
    path1 = os.path.join(folder, master_name + extension)
    path2 = os.path.join(folder, slave_name + extension)
    outfile_folder = common.get_work_folder("gap")

    warn = False

    tables = common.get_common_tables(
        settings_db1, settings_db2)

    for table in tables:
        common.extract_to_csv(
            settings_db1[1], table, path1, segment, fetch)

        common.extract_to_csv(
            settings_db2[1], table, path2, segment, fetch)

        if mode == "hash":
            hash1 = common.get_hash_file(path1)
            hash2 = common.get_hash_file(path2)
            if hash1 != hash2:
                warn = True
                logs.log_warn(f"Gap found for table {table}")

        else:
            duck.load_file_data(
                filename=path1, tablename=master_name)
            duck.load_file_data(
                filename=path2, tablename=slave_name)

            query = f"""(SELECT '{settings_db1[2]}' as DATABASE, *
            FROM {master_name}
            EXCEPT SELECT '{settings_db1[2]}', * FROM {slave_name})
            UNION
            (SELECT '{settings_db2[2]}' as DATABASE, * FROM {slave_name}
            EXCEPT SELECT '{settings_db2[2]}', * FROM {master_name})"""

            data = duck.get_datas_by_fetchdf(query)

            if mode == "column":
                differences = common.find_most_similar_pairs(data)
                if len(differences) > 0:
                    path_outfile = os.path.join(
                        outfile_folder, f"gap_{table}.txt")
                    common.create_gap_files(path_outfile, differences)
                    warn = True
            else:
                if isinstance(data, pandas.DataFrame):
                    if not data.empty:
                        path_outfile = os.path.join(
                            outfile_folder, f"gap_{table}.csv")
                        common.create_gap_files(path_outfile, data)
                        warn = True

            duck.delete_tmp_db()
            common.delete_work_folder("extracts")

    if warn:
        raise exceptions.Warn(300)

    return 201
