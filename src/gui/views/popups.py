# -*- coding: utf-8 -*-

"""
Module: popups
Auteur: creagleone
Date: 2025-05-07

Description:
    This module contains functions to manage custom exceptions

Dépendances:
    - QtWidgets (PySide6)
    - QtCore (PySide6)

Usage Example:
    popups.give_error(title, message)

Notes:
    - N/A
"""

from PySide6 import QtWidgets, QtCore


def select_files():
    """
    File selection popup

    Returns:
        text: if OK else None
    """
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly
    files, _ = QtWidgets.QFileDialog.getOpenFileNames(
        None, "Select files",
        QtCore.QDir.currentPath(),
        "All files (*.*);;Text files (*.txt)",
        options=options)

    return files


def display_info(message):
    """
    information popup

    Args:
        title (str): popup title
        title (str): popup message
    """
    title = QtCore.QCoreApplication.translate(
        "exceptions", "Success")
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.exec()


def display_warn(message, test=True):
    """
    Warning popup

    Args:
        title (str): popup title
        message (str): popup message
    """
    title = QtCore.QCoreApplication.translate(
        "exceptions", "An alert has occured")
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Warning)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    if test:
        msg_box.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    else:
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    response = msg_box.exec()

    if response == QtWidgets.QMessageBox.No:
        return False
    return True


def display_error(message):
    """
    Error popup

    Args:
        title (str): popup title
        title (str): popup message
    """
    title = QtCore.QCoreApplication.translate(
        "exceptions", "An error has occured")
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.exec()


def input_value(title: str, message: str):
    """
    Input popup

    Args:
        title (str): popup title
        title (str): popup message

    Returns:
        text: if OK else None
    """
    text, ok = QtWidgets.QInputDialog.getText(None, title, message)
    if ok:
        return text
    return None
