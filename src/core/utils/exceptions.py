# -*- coding: utf-8 -*-

"""
Module: exceptions
Auteur: creagleone
Date: 2025-05-07

Description:
    This module contains functions to manage custom exceptions

Dependencies:
    - QtCore (PySide6)
    - logs.py

Usage Example:
    raise Error(100, "texte")

Notes:
    - N/A
"""

from PySide6 import QtCore
from core.utils import logs

# MESSAGES = {
#     100: QtCore.QCoreApplication.translate(
#         "exceptions", "Backup successfully"),
#     200: QtCore.QCoreApplication.translate(
#         "exceptions", "Treatment completed successfully"),
#     201: QtCore.QCoreApplication.translate(
#         "exceptions", "No discrepancies were found"),

#     300: QtCore.QCoreApplication.translate(
#         "exceptions", "Discrepancies were found"),

#     400: QtCore.QCoreApplication.translate(
#         "exceptions", "Poorly formed or invalid SQL query"),
#     401: QtCore.QCoreApplication.translate(
#         "exceptions", "An error was occured"),
#     402: QtCore.QCoreApplication.translate(
#         "exceptions", "UNIQUE constraint failed"),
#     403: QtCore.QCoreApplication.translate(
#         "exceptions", "Syntax error"),
#     404: QtCore.QCoreApplication.translate(
#         "exceptions", "Table or column not found"),
#     405: QtCore.QCoreApplication.translate(
#         "exceptions", "Incorrect database config"),
#     406: QtCore.QCoreApplication.translate(
#         "exceptions", "Data type mismatch"),
#     407: QtCore.QCoreApplication.translate(
#         "exceptions", "Conversion error"),
#     408: QtCore.QCoreApplication.translate(
#         "exceptions", "Transaction error"),

#     500: QtCore.QCoreApplication.translate(
#         "exceptions", "Failed to connect to database"),
#     501: QtCore.QCoreApplication.translate(
#         "exceptions", "Database temporarily unavailable"),
#     502: QtCore.QCoreApplication.translate(
#         "exceptions", "Out of memory error"),
#     503: QtCore.QCoreApplication.translate(
#         "exceptions", "Disk I/O error"),
#     504: QtCore.QCoreApplication.translate(
#         "exceptions", "No active Oracle listener"),
#     505: QtCore.QCoreApplication.translate(
#         "exceptions", "Account locked"),
#     506: QtCore.QCoreApplication.translate(
#         "exceptions", "Incorrect username or password"),

#     600: QtCore.QCoreApplication.translate(
#         "exceptions", "System not supported"),
#     601: QtCore.QCoreApplication.translate(
#         "exceptions", "Settings file not found"),
#     602: QtCore.QCoreApplication.translate(
#         "exceptions", "Themes file not found"),
#     603: QtCore.QCoreApplication.translate(
#         "exceptions", "No tables to compare"),

#     999: QtCore.QCoreApplication.translate(
#         "exceptions", "Unanticipated error - check logs"),
# }


class ErrorSignal(QtCore.QObject):
    """
    A Qt object that provides an error signaling mechanism
    """

    error_signal = QtCore.Signal(str)

    def trigger_error(self, message: str) -> None:
        """
        Triggers an error signal with the given message

        Args:
            message (str): The error message to send
        """
        QtCore.QMetaObject.invokeMethod(self, "emit_error",
                                        QtCore.Q_ARG(str, message))

    @QtCore.Slot(str)
    def emit_error(self, message: str) -> None:
        """
        Emits the error signal and logs the error message

        Args:
            message (str): The error message to emit and log
        """
        self.error_signal.emit(message)
        logs.log_error(message)


class WarnSignal(QtCore.QObject):
    """
    A Qt object that provides a warning signaling mechanism
    """

    warn_signal = QtCore.Signal(str)

    def trigger_warn(self, message: str) -> None:
        """
        Triggers a warning signal with the given message

        Args:
            message (str): The warning message to send
        """
        QtCore.QMetaObject.invokeMethod(self, "emit_warn",
                                        QtCore.Q_ARG(str, message))

    @QtCore.Slot(str)
    def emit_warn(self, message: str) -> None:
        """
        Emits the warning signal and logs the warning message

        Args:
            message (str): The warning message to emit and log
        """
        self.warn_signal.emit(message)
        logs.log_warn(message)


class Error(Exception):
    """
    Custom exception class that integrates logging and Qt
    error signaling
    """

    def __init__(self, code: str, system: str | None = None) -> None:
        """
        Initializes the exception with an error message and triggers
        error logging

        Args:
            code (str): The error code used to fetch the corresponding message
            system (str | None, optional): System context for logging
        """

        self.errors = {
            400: QtCore.QCoreApplication.translate(
                "exceptions", "Poorly formed or invalid SQL query"),
            401: QtCore.QCoreApplication.translate(
                "exceptions", "An error was occured"),
            402: QtCore.QCoreApplication.translate(
                "exceptions", "UNIQUE constraint failed"),
            403: QtCore.QCoreApplication.translate(
                "exceptions", "Syntax error"),
            404: QtCore.QCoreApplication.translate(
                "exceptions", "Table or column not found"),
            405: QtCore.QCoreApplication.translate(
                "exceptions", "Incorrect database config"),
            406: QtCore.QCoreApplication.translate(
                "exceptions", "Data type mismatch"),
            407: QtCore.QCoreApplication.translate(
                "exceptions", "Conversion error"),
            408: QtCore.QCoreApplication.translate(
                "exceptions", "Transaction error"),

            500: QtCore.QCoreApplication.translate(
                "exceptions", "Failed to connect to database"),
            501: QtCore.QCoreApplication.translate(
                "exceptions", "Database temporarily unavailable"),
            502: QtCore.QCoreApplication.translate(
                "exceptions", "Out of memory error"),
            503: QtCore.QCoreApplication.translate(
                "exceptions", "Disk I/O error"),
            504: QtCore.QCoreApplication.translate(
                "exceptions", "No active Oracle listener"),
            505: QtCore.QCoreApplication.translate(
                "exceptions", "Account locked"),
            506: QtCore.QCoreApplication.translate(
                "exceptions", "Incorrect username or password"),

            600: QtCore.QCoreApplication.translate(
                "exceptions", "System not supported"),
            601: QtCore.QCoreApplication.translate(
                "exceptions", "Settings file not found"),
            602: QtCore.QCoreApplication.translate(
                "exceptions", "Themes file not found"),
            603: QtCore.QCoreApplication.translate(
                "exceptions", "No tables to compare"),
            604: QtCore.QCoreApplication.translate(
                "exceptions", "Error occurring during data extraction"),

            999: QtCore.QCoreApplication.translate(
                "exceptions", "Unanticipated error - check logs"),
        }

        self.message = self.errors.get(
            code, QtCore.QCoreApplication.translate(
                "exceptions", "Unknown code"
            )
        )
        super().__init__(self.message)

        if system is not None:
            logs.log_error(system)

        self.qt_error = ErrorSignal()
        self.qt_error.trigger_error(self.message)


class Warn(Exception):
    """
    Custom warning exception that integrates logging and Qt warning signaling
    """

    def __init__(self, code: str) -> None:
        """
        Initializes the warning exception with a message and triggers
        warning signaling

        Args:
            code (str): The warning code used to fetch the
            corresponding message
        """
        super().__init__(code)

        self.warn = {
            300: QtCore.QCoreApplication.translate(
                "exceptions", "Discrepancies were found"),
        }

        self.message = self.warn.get(
            code, QtCore.QCoreApplication.translate(
                "exceptions", "Unknown code"
            )
        )

        self.qt_warn = WarnSignal()
        self.qt_warn.trigger_warn(self.message)


class INFO:
    def __init__(self, code: str) -> None:
        """
        Initializes the info with a message and triggers
        info signaling

        Args:
            code (str): The info code used to fetch the
            corresponding message
        """

        self.info = {
            100: QtCore.QCoreApplication.translate(
                "exceptions", "Backup successfully"),
            101: QtCore.QCoreApplication.translate(
                "exceptions", "Backup successfully"),
            200: QtCore.QCoreApplication.translate(
                "exceptions", "Treatment completed successfully"),
            201: QtCore.QCoreApplication.translate(
                "exceptions", "No discrepancies were found"),
        }

        self.message = self.info.get(
            code, QtCore.QCoreApplication.translate(
                "exceptions", "Unknown code"
            )
        )

    def __str__(self):
        return self.message
