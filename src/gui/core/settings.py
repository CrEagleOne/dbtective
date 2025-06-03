# -*- coding: utf-8 -*-

"""
Module: settings
Author: creagleone
Date: 2025-05-07

Description:
    This module contains functions to recover system settings

Dependencies:
    - os
    - json
    - common.py

Usage Example:
    - Settings().get_settings()
    - Settings().get_settings("key")

Notes:
    - N/A
"""

import os
import json
from core.utils import common


class Settings:
    """
    Manages application settings stored in a JSON file
    """

    def __init__(self):
        """
        Initializes the Settings class by loading existing settings
        """
        super().__init__()

        json_file = "src/settings.json"
        app_path = common.resource_path(json_file)
        self.settings_path = os.path.normpath(app_path)

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
            key (str | None): The key to look up. Returns all settings if None

        Returns:
            dict | str: The requested setting value or full
            settings dictionary
        """
        return self.items if key is None else self.items.get(key)
