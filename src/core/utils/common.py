# -*- coding: utf-8 -*-

"""
Module: common
Auteur: creagleone
Date: 2025-05-07
Description:
    This module contains functions to manage technical tables

Dependencies:
    - os
    - sys
    - shutil
    - re
    - hashlib
    - gzip
    - csv
    - tempfile
    - platform
    - subprocess
    - pandas
    - QtWidgets (PySide6)
    - oracle.py
    - exceptions.py

Usage Example:
    update_style(widget, "border", "2px solid red")

Notes:
    - N/A
"""

import os
import sys
import shutil
import re
import hashlib
import gzip
import csv
import tempfile
import platform
import subprocess
import pandas
from PySide6 import QtWidgets
from core.database import oracle
from core.utils import exceptions

sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..")))


def get_file_size(filepath: str) -> str:
    """
    Retrieves the file size and dynamically chooses the most suitable unit

    Args:
        filepath (str): Filenmae

    Returns:
        str: File size with the most suitable unit
    """
    taille_octets = os.path.getsize(filepath)

    if taille_octets < 1024:
        return f"{taille_octets} octets"
    if taille_octets < 1024**2:
        return f"{taille_octets / 1024:.2f} Ko"
    if taille_octets < 1024**3:
        return f"{taille_octets / (1024**2):.2f} Mo"
    return f"{taille_octets / (1024**3):.2f} Go"


def merge_common_keys(dict1: list, dict2: list) -> dict:
    """
    Merges data from 2 dict for each common key

    Args:
        dict1 (list): dict1
        dict2 (list): dict2

    Returns:
        dict: Merge dict
    """

    dict1_tmp = {key: list(values) for key, *values in dict1}
    dict2_tmp = {key: list(values) for key, *values in dict2}

    common_keys = set(dict1_tmp.keys()) & set(dict2_tmp.keys())

    merged_dict = {}
    for key in common_keys:
        values1 = dict1_tmp[key]
        values2 = dict2_tmp[key]
        merged_values = [val for pair in zip(values1, values2) for val in pair]
        merged_dict[key] = merged_values

    return merged_dict


def get_hash_file(filepath: str, hash_algorithm: str = 'sha256') -> str:
    """
    Calculate the hash of a file using the specified algorithm

    Args:
        filepath (str): File path.
        hash_algorithm (str): Hash algorithm to use. Defaults to 'sha256'.

    Returns:
        str: File hash
    """
    hasher = hashlib.new(hash_algorithm)
    open_func = gzip.open if filepath.endswith('.gz') else open
    with open_func(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_tables_of_db(db_config: list) -> tuple:
    """
    Retrieve the list of tables, their size, the number of columns and rows

    Args:
        db_config (list): Database config

    Returns:
        dict: Database content
    """
    if db_config[0] == "Oracle":
        query = """
            SELECT
                ut.TABLE_NAME,
                ut.NUM_ROWS AS "Nombre de lignes",
                COUNT(utc.COLUMN_NAME) AS "Nombre de colonnes",
                ut.BLOCKS * ut.AVG_ROW_LEN AS "Taille estimée (octets)"
            FROM USER_TABLES ut
            LEFT JOIN USER_TAB_COLUMNS utc ON ut.TABLE_NAME = utc.TABLE_NAME
            GROUP BY ut.TABLE_NAME, ut.NUM_ROWS, ut.BLOCKS, ut.AVG_ROW_LEN"""
        return oracle.get_list_data(db_config[1], query)
    raise exceptions.Error(405)


def get_common_tables(db1: list, db2: list) -> dict:
    """
    Retrieve the common tables of 2 bases

    Args:
        db1 (list): Database 1 configuration
        db2 (list): Database 2 configuration

    Returns:
        dict: Common tables
    """
    db1_tables = get_tables_of_db(db1)
    db2_tables = get_tables_of_db(db2)

    return merge_common_keys(db1_tables, db2_tables)


def extract_to_csv(db: list, table: str, file: str, segment_size: int | None,
                   fetch_size: int):
    """
    Extract data to a CSV file

    Args:
        db (list): Database configuration
        table (str): Tablename
        file (str): Output file name

    """
    query = f"SELECT * FROM {table}"

    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        datas = oracle.get_data_by_segment(
            db, segment_size, fetch_size, query)
        for data_block in datas:
            writer.writerows(data_block)


def update_style(widget: QtWidgets.QWidget, property_name: str,
                 new_value: str):
    """
    Modify a widget's stylesheet by updating or adding a CSS property

    Args:
        widget (QWidget): Target widget to update
        property_name (str): CSS property name (e.g., "background-color")
        new_value (str): New value for the property (e.g., "red", "20px")

    Notes:
        - If the property exists, its value is replaced
        - If absent, the property is appended to the stylesheet
    """

    style = widget.styleSheet()

    if f"{property_name}:" in style:
        style = re.sub(f"{property_name}: .*?;",
                       f"{property_name}: {new_value};", style)
    else:
        style += f" {property_name}: {new_value};"

    widget.setStyleSheet(style)


def resource_path(relative_path: str) -> str:
    """
    Returns the absolute path to a resource file based on the
    current directory

    If the application is built with PyInstaller,
    this function returns the path to the _MEIPASS folder to find
    resource files
    Otherwise, this function returns the path to the current directory to find
    resource files

    Parameters :
        relative_path (str) : The relative path of a resource file.

    Returns :
        str : The absolute path to a resource file.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def set_svg_icon(icon_name: str) -> str:
    """
    Returns the absolute path to an SVG used as an icon.

    Parameters :
        icon_name (str) : The name of the icon.

    Returns :
        str : The path to the SVG icon.
    """
    folder = "src/gui/images/svg_icons/"
    path = resource_path(folder)
    icon = os.path.normpath(os.path.join(path, icon_name))
    return icon


def set_svg_image(icon_name: str) -> str:
    """
    Returns the absolute path to an SVG image used in the graphical
    user interface

    Parameters :
        icon_name (str) : The name of the icon.

    Returns :
        str : The path to the SVG image.
    """
    folder = "src/gui/images/svg_images/"
    path = resource_path(folder)
    icon = os.path.normpath(os.path.join(path, icon_name))
    return icon


def set_image(image_name: str) -> str:
    """
    Returns the absolute path to an image used in the graphical
    user interface

    Parameters :
        icon_name (str) : The name of the icon.

    Returns :
        str : The path to the image.
    """
    folder = "src/gui/images/images/"
    path = resource_path(folder)
    image = os.path.normpath(os.path.join(path, image_name))
    return image


def create_gap_files(filename: str, data: pandas.DataFrame):
    """
    Create a csv file containing the data discrepancies

    Args:
        filename (str): Path of the file to write
        data (pd.DataFrame): Data to write
    """
    if filename.endswith('csv'):
        data.to_csv(filename, header=True, index=False, mode='w')
    else:
        with open(filename, 'w', encoding='UTF-8') as f:
            for diff in data:
                pair, diff_set = diff
                f.write(f"Paire: {pair}\n")
                f.write(f"Différences: {diff_set}\n\n")


def get_work_files(path: str) -> str:
    """
    Get the working file path inside the system's temporary directory

    Args:
        path (str): The relative path inside the work directory

    Returns:
        str: The full path inside the temporary workspace
    """
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, "dbtective", path)


def get_work_folder(path: str) -> str:
    """
    Get the working folder path inside the system's temporary directory
    Creates the folder if it does not exist

    Args:
        path (str): The relative path inside the work directory

    Returns:
        str: The full path inside the temporary workspace
    """
    temp_dir = tempfile.gettempdir()
    work_folder = os.path.join(temp_dir, "dbtective", path)
    os.makedirs(work_folder, exist_ok=True)

    return work_folder


def delete_work_folder(path: str):
    """
    Deletes all files and subdirectories inside a temporary work folder
    and recreates an empty version of it

    Args:
        path (str): The relative path inside the 'dbtective' temp directory
                    to be purged
    """
    temp_dir = tempfile.gettempdir()
    work_folder = os.path.join(temp_dir, "dbtective", path)
    shutil.rmtree(work_folder)
    os.makedirs(work_folder)


def open_folders(folder: str):
    """
    Ouvrir un fichier avec un éditeur de fichier

    Args:
        filename (str): Nom du fichier.
    """
    system = platform.system()

    if system == "Windows":
        subprocess.run(f'explorer "{folder}"', shell=True, check=False)
    elif system == "Linux":
        subprocess.run(["xdg-open", folder], check=False)
    elif system == "Darwin":
        subprocess.run(["open", folder], check=False)
    else:
        raise exceptions.Error(600, system)


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculate the Levenshtein distance between two strings

    The Levenshtein distance is a measure of the difference between
    two sequences, which is defined as the minimum number of
    single-character edits (insertions, deletions, or substitutions)
    required to change one sequence into the other

    Parameters:
    s1 (str): The first string to compare
    s2 (str): The second string to compare

    Returns:
    int: The Levenshtein distance between s1 and s2
    """
    if len(s1) < len(s2):
        s1, s2 = s2, s1

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def compare_pairs(pairs: list) -> list:
    """
    Compare pairs of comma-separated strings and return the symmetric
    difference between their elements

    Args:
        pairs (list[tuple[str, str]]): A list of tuples, where each tuple
                                        contains two comma-separated strings
                                        to compare

    Returns:
        list: A list of tuples :
                - The original pair of strings
                - A set containing the symmetric difference between elements
                    of both strings
    """
    differences = []
    for pair in pairs:
        s1, s2 = pair
        set1 = set(s1.split(','))
        set2 = set(s2.split(','))
        diff = set1.symmetric_difference(set2)
        differences.append((pair, diff))
    return differences


def merge_columns(row: pandas.Series) -> str:
    """
    Converts a pandas Series row into a comma-separated string

    Args:
        row (pandas.Series): A pandas row containing values to merge

    Returns:
        str: A single string with all row values joined by commas
    """
    return ','.join(row.astype(str))


def find_most_similar_pairs(df: pandas.DataFrame,
                            column: str = 'merged') -> list:
    """
    Finds the most similar pairs in a DataFrame column using
    Levenshtein distance

    Args:
        df (pandas.DataFrame): The DataFrame containing the column to compare
        column (str, optional): The name of the column, defaults to 'merged'

    Returns:
        list[tuple[tuple[str, str], set[str]]]: A list of tuples with:
            - The pair of most similar strings
            - A set indicating their symmetric differences
    """
    df[column] = df.apply(merge_columns, axis=1)
    pairs = set()
    for i in range(len(df)):
        s1 = df.iloc[i][column]
        min_distance = float('inf')
        most_similar = None
        for j in range(len(df)):
            if i != j:
                s2 = df.iloc[j][column]
                distance = levenshtein_distance(s1, s2)
                if distance < min_distance:
                    min_distance = distance
                    most_similar = s2
        pair = tuple(sorted([s1, most_similar]))
        pairs.add(pair)

    differences = compare_pairs(list(pairs))
    return differences
