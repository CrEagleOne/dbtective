# -*- coding: utf-8 -*-

"""
Module: common
Author: creagleone
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
    - from_path (charset_normalizer)
    - QtWidgets (PySide6)
    - oracle.py
    - exceptions.py
    - config.py

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
from charset_normalizer import from_path
from PySide6 import QtWidgets
from core.database import oracle
from core.utils import exceptions, config


def get_file_size(filepath: str) -> str:
    """
    Retrieves the file size

    Args:
        filepath (str): Path of file

    Returns:
        str: File size with the most suitable unit
    """
    size = os.path.getsize(filepath)

    return get_suitable_unit_for_size(size)


def get_suitable_unit_for_size(size: int) -> str:
    """
    Dynamically chooses the most suitable unit

    Args:
        size (int): Size value

    Returns:
        str: File size with the most suitable unit
    """
    if size < 1024:
        return f"{size} octets"
    if size < 1024**2:
        return f"{size / 1024:.2f} Ko"
    if size < 1024**3:
        return f"{size / (1024**2):.2f} Mo"
    return f"{size / (1024**3):.2f} Go"


def merge_common_keys(dict1: tuple, dict2: tuple) -> dict:
    """
    Merges data from 2 dict for each common key

    Args:
        dict1 (tuple): dict1
        dict2 (tuple): dict2

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
        merged_values = [abs(v1 - v2) for v1, v2 in zip(values1, values2)]
        merged_values[0] = get_suitable_unit_for_size(int(merged_values[0]))
        merged_dict[key] = merged_values

    return merged_dict


def get_hash_file(filepath: str, hash_algorithm: str = 'sha256') -> str:
    """
    Calculate the hash of a file using the specified algorithm

    Args:
        filepath (str): File path
        hash_algorithm (str): Hash algorithm to use. Defaults to 'sha256'

    Returns:
        str: File hash
    """
    hasher = hashlib.new(hash_algorithm)
    open_func = gzip.open if filepath.endswith('.gz') else open
    with open_func(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_tables_of_db(db_config: list) -> list:
    """
    Retrieve the list of tables, their size, the number of columns and rows

    Args:
        db_config (list): Database config

    Returns:
        list: Database content
    """
    result = []
    if db_config[0] == "Oracle":
        query = """
            SELECT
                ut.TABLE_NAME,
                ut.BLOCKS * ut.AVG_ROW_LEN,
                COUNT(utc.COLUMN_NAME),
                ut.NUM_ROWS
            FROM USER_TABLES ut
            LEFT JOIN USER_TAB_COLUMNS utc ON ut.TABLE_NAME = utc.TABLE_NAME
            GROUP BY ut.TABLE_NAME, ut.NUM_ROWS, ut.BLOCKS, ut.AVG_ROW_LEN"""
        result = oracle.get_list_data(db_config[1], query)
    elif db_config[0] == "CSV":
        for file_path in db_config[1]["file"]:
            result.append(analyze_file(file_path))
    else:
        raise exceptions.Error(405)

    return result


def get_common_tables(db1: list, db2: list) -> dict:
    """
    Retrieve common tables from 2 data sources
    Tables must have the same name, including CSV files.

    Args:
        db1 (list): Database 1 configuration
        db2 (list): Database 2 configuration

    Returns:
        dict: Common tables
    """
    db1_tables = get_tables_of_db(db1)
    db2_tables = get_tables_of_db(db2)

    return merge_common_keys(db1_tables, db2_tables)


def oracle_to_csv(db: list, table: str, file: str, segment_size: int | None,
                  fetch_size: int):
    """
    Extract data to a CSV file

    Args:
        db (list): Database configuration
        table (str): Tablename
        file (str): Output file name

    """
    query = f"""SELECT * FROM {table}"""

    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        datas = oracle.get_data_by_segment(
            db, segment_size, fetch_size, query)
        for data_block in datas:
            writer.writerows(data_block)


def convert_to_csv(src_file: str, dest_file: str):
    """
    Copies a file to a specified directory
    and converts it to CSV format if necessary.

    Args:
        src_file (str): The full path to the source file to be copied.
                        Supported formats: .txt, .xlsx, .csv
        dest_file (str): The path to the destination directory
    """
    file_extension = os.path.splitext(src_file)[1].lower()

    if file_extension == '.txt':
        with open(src_file, 'r', encoding='UTF-8') as f:
            content = f.read()
        with open(dest_file, 'w', encoding='UTF-8') as f:
            f.write(content)
    elif file_extension == '.xlsx':
        df = pandas.read_excel(src_file, header='infer',
                               engine='openpyxl', dtype=str,
                               na_values=[], keep_default_na=False)
        df.to_csv(dest_file, index=False)
    elif file_extension == '.csv':
        df = pandas.read_csv(src_file, sep=None,
                             header='infer', engine='python', dtype=str,
                             na_values=[], keep_default_na=False)
        df.to_csv(dest_file, index=False)
    else:
        raise exceptions.Error(605, file_extension)


def analyze_file(file_path: str) -> tuple:
    """
    Analyze file to extract some datas

    Args:
        file_path (str): Path of file
                        Supported formats: .txt, .xlsx, .csv

    Raises:
        exceptions.Error: 605 or 606

    Returns:
        tuple: datas
    """
    try:
        file_size = os.path.getsize(file_path)
    except FileNotFoundError:
        raise exceptions.Error(608)
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.csv':
        df = pandas.read_csv(file_path, sep=None,
                             header='infer', engine='python')
    elif ext == '.txt':
        df = pandas.read_csv(file_path, sep=None,
                             header='infer', engine='python')
    elif ext == '.xlsx':
        df = pandas.read_excel(file_path, header='infer', engine='openpyxl')
    else:
        raise exceptions.Error(605)

    num_rows, num_cols = df.shape
    if df.columns.to_list() == list(range(len(df.columns))):
        raise exceptions.Error(606)

    return (
        os.path.splitext(os.path.basename(file_path))[0],
        file_size,
        num_cols,
        num_rows
    )


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
        relative_path (str) : The relative path of a resource file

    Returns :
        str : The absolute path to a resource file
    """
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', '..'))

    full_path = os.path.join(base_path, relative_path)

    if not os.path.exists(full_path):
        raise exceptions.Error(
            601, f"{full_path} not found")

    return full_path


def set_svg_icon(icon_name: str) -> str:
    """
    Returns the absolute path to an SVG used as an icon

    Parameters :
        icon_name (str) : The name of the icon

    Returns :
        str : The path to the SVG icon
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
        icon_name (str) : The name of the icon

    Returns :
        str : The path to the SVG image
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
        icon_name (str) : The name of the icon

    Returns :
        str : The path to the image.
    """
    folder = "src/gui/images/images/"
    path = resource_path(folder)
    image = os.path.normpath(os.path.join(path, image_name))
    return image


def set_locale(translate_name: str) -> str:
    """
    Returns the absolute path of the application translation file

    Parameters :
        icon_name (str) : The name of the icon

    Returns :
        str : The path to the image.
    """
    folder = "src/gui/locales/"
    path = resource_path(folder)
    translate_file = os.path.normpath(os.path.join(path, translate_name))
    return translate_file


def create_gap_files(filename: str, data: pandas.DataFrame):
    """
    Create a csv file containing the data discrepancies

    Args:
        filename (str): Path of the file to write
        data (pandas.DataFrame): Data to write
    """
    if filename.endswith('csv'):
        data.to_csv(filename, header=True, index=False, mode='w')
    else:
        with open(filename, 'w', encoding='UTF-8') as f:
            for diff in data:
                pair, diff_set = diff
                f.write(f"Paire: {pair}\n")
                f.write(f"Différences: {diff_set}\n\n")


def get_file_in_work_folder(path: str) -> str:
    """
    Get the working folder path inside the system's temporary directory
    Creates the folder if it does not exist

    Args:
        path (str): The relative path inside the work directory

    Returns:
        str: The full path inside the temporary workspace
    """
    temp_dir = tempfile.gettempdir()
    work_folder = os.path.join(temp_dir, "dbtective")
    os.makedirs(work_folder, exist_ok=True)

    return os.path.join(work_folder, path)


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
    Open a file with a file editor

    Args:
        filename (str): File name
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
        set1 = set(s1.split(',')[1:])
        set2 = set(s2.split(',')[1:])
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
        list: A list of tuples :
                - The original pair of strings
                - A set containing the symmetric difference between elements
                    of both strings
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


def get_current_locale() -> str:
    """
    Retrieves the current locale setting from the configuration

    Returns:
        str: The current locale setting
    """
    query = "SELECT [values] from settings where [key] = ?"
    return config.get_settings(query, ("locale",))


def get_all_locales(path="src/gui/locales") -> list:
    """
    Retrieves all available locales from the specified directory

    Args:
        path (str, optional): The path to the directory containing locale files

    Returns:
        list: A list of available locales, with the current locale first
    """
    locale = get_current_locale()
    folder = resource_path(path)
    translations = ["en_US"] + [os.path.splitext(f)[0] for f in os.listdir(
        folder) if f.endswith(".qm")]

    translations = [f for f in translations if f != locale]

    return [locale] + translations


def is_data_table(file_path):
    """Check if the given file is a valid data table.

    This function attempts to read the file using pandas and checks whether 
    it contains both columns and rows. (CSV only)

    Args:
        file_path (str): Path to the data file

    Returns:
        bool: True if the file is a valid data table, False otherwise
    """
    try:
        if os.path.splitext(file_path)[1].lower() != ".csv":
            return False
        result = from_path(file_path)
        encoding = result.best().encoding if result.best() else "ISO-8859-1"

        df = pandas.read_csv(file_path, sep=None,
                             engine="python", encoding=encoding)

        if not df.empty and not df.columns.empty:
            return True

        return False
    except Exception as e:
        print(f"Error reading the file: {e}")
        return False
