# -*- coding: utf-8 -*-

"""
Module: themes
Auteur: creagleone
Date: 2025-05-07

Description:
    This module contains functions to recover theme settings

Dependencies:
    - os
    - json
    - settings.py
    - common.py
    - exceptions.py

Usage Example:
    - Themes().get_theme()

Notes:
    - N/A
"""

import os
import json
from gui.core import settings
from core.utils import common, exceptions


class Themes():
    """
    Manages application settings stored in a JSON file
    """

    def __init__(self):
        """
        Initializes the Settings class by loading existing settings
        """
        super().__init__()

        _settings = settings.Settings().get_settings()
        json_file = f"src/gui/themes/{_settings['theme_name']}.json"
        app_path = common.resource_path(json_file)
        self.settings_path = os.path.normpath(app_path)
        if not os.path.isfile(self.settings_path):
            raise exceptions.Error(
                602,
                f"""{_settings['theme_name']}.json not found in
                    {self.settings_path}""")

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

    def get_theme(self, key: str | None = None) -> dict | str:
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
