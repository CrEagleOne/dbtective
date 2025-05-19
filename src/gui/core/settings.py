# -*- coding: utf-8 -*-

"""
Module: settings
Auteur: creagleone
Date: 2025-05-07
Description:
    This module contains functions to recover system settings

Dependencies:
    - os
    - json
    - common.py
    - exceptions.py

Usage Example:
    - Settings().get_settings()
    - Settings().get_settings("key")

Notes:
    - N/A
"""

import os
import json
from core.utils import common, exceptions


class Settings:
    """
    Manages application settings stored in a JSON file

    Attributes:
        json_file (str): The settings file name
        app_path (str): The absolute path to the settings file
        settings_path (str): The normalized path for accessing the settings
        items (dict): Dictionary holding the loaded settings
    """
    json_file = "src/settings.json"
    app_path = os.path.abspath(os.getcwd())
    app_path = common.resource_path(json_file)
    settings_path = os.path.normpath(app_path)
    if not os.path.isfile(settings_path):
        raise exceptions.Error(
            601, f"{json_file} not found in {settings_path}")

    def __init__(self):
        """
        Initializes the Settings class by loading existing settings
        """
        super().__init__()

        self.items = {}
        self.deserialize()

    def serialize(self):
        """
        Saves the current settings to the settings file in JSON format
        """
        with open(self.settings_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)

    def deserialize(self):
        """
        Loads settings from the JSON file and stores them in the
        `items` dictionary
        """
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            self.items = json.loads(reader.read())

    def get_settings(self, key: str = None):
        """
        Retrieves a specific setting or the entire settings dictionary

        Args:
            key (str | None, optional): The key to look up. Returns all
            settings if None

        Returns:
            dict | str: The requested setting value or full
            settings dictionary
        """
        return self.items if key is None else self.items.get(key)
