# -*- coding: utf-8 -*-

"""
Module: logs
Author: creagleone
Date: 2025-05-07

Description:
    This module contains functions to manage logs

Dependencies:
    - os
    - logging
    - tempfile
    - partial (functools)
    - settings.py

Usage Example:
    log_error(message)

Notes:
    - N/A
"""

import os
import logging
import tempfile
from functools import partial
from gui.core import settings


def log_config() -> None:
    """
    Configures the logging system based on user settings

    - Retrieves the log level from the settings
    - Creates a temporary directory for log storage
    - Sets up logging with file and console handlers

    Returns:
        None
    """
    log_level = settings.Settings().get_settings(key='log_level')
    temp_dir = tempfile.gettempdir()
    log_path = os.path.join(temp_dir, "dbtective", "app.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format='%(asctime)s %(levelname)s:%(message)s',
        handlers=[
            logging.FileHandler(log_path, encoding='utf-8', mode='a'),
            logging.StreamHandler()
        ]
    )


def log_message(log_level, message):
    """
    Log a message with the specified level

    Args:
        log_level (str): Log level ('error', 'info', 'warning', 'debug')
        message (str): Message text
    """
    logger = {
        "error": logging.error,
        "info": logging.info,
        "warning": logging.warning,
        "debug": logging.debug,
    }
    if log_level in logger:
        logger[log_level](message)


log_error = partial(log_message, "error")
log_info = partial(log_message, "info")
log_warn = partial(log_message, "warning")
log_debug = partial(log_message, "debug")
log_critical = partial(log_message, "critical")
