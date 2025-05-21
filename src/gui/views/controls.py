# -*- coding: utf-8 -*-

"""
Module: controls
Auteur: creagleone
Date: 2025-05-07

Description:
    This module contains functions to controls input datas

Dependencies:
    - QtCore (PySide6)
    - common.py

Usage Example:
    - N/A

Notes:
    - N/A
"""
from PySide6 import QtCore
from core.utils import common


def init_oracle(self):
    """
    Init UI of the input data for oracle settings
    """
    self.ui.saveDB.setEnabled(False)
    self.ui.testDB.setEnabled(False)
    self.ui.logbar.log_label.setText("")
    common.update_style(self.ui.logbar.log_label, "color",
                        self.themes["app_color"]["text_description"])

    common.update_style(self.ui.setHostOracle, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setPortOracle, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setDBOracle, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setSIDOracle, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setUsernameOracle, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setPasswordOracle, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setCustomName, "border",
                        "2px solid transparent")


def oracle(self):
    """
    Control the input data for oracle settings
    """
    init_oracle(self)
    error = False
    if not self.ui.setHostOracle.text():
        common.update_style(self.ui.setHostOracle,
                            "border", "2px solid red")
        error = True

    if not self.ui.setPortOracle.text():
        common.update_style(self.ui.setPortOracle,
                            "border", "2px solid red")
        error = True

    if not self.ui.setDBOracle.text():
        common.update_style(self.ui.setDBOracle, "border", "2px solid red")
        error = True

    if not self.ui.setSIDOracle.currentText():
        common.update_style(self.ui.setSIDOracle,
                            "border", "2px solid red")
        error = True

    if not self.ui.setUsernameOracle.text():
        common.update_style(self.ui.setUsernameOracle,
                            "border", "2px solid red")
        error = True

    if not self.ui.setPasswordOracle.text():
        common.update_style(self.ui.setPasswordOracle,
                            "border", "2px solid red")
        error = True

    if not error:
        self.ui.testDB.setEnabled(True)

    if not self.ui.setCustomName.text():
        common.update_style(self.ui.setCustomName,
                            "border", "2px solid red")
        error = True

    if not error:
        self.ui.saveDB.setEnabled(True)
        return
    self.ui.logbar.log_label.setText("Corriger les erreurs")
    common.update_style(self.ui.logbar.log_label, "color", "red")


def init_db_compare(self):
    """
    Init UI of the input data for database comparison
    """
    self.ui.compare.setEnabled(False)
    self.ui.logbar.log_label.setText("")

    common.update_style(self.ui.logbar.log_label, "color",
                        self.themes["app_color"]["text_description"])

    common.update_style(self.ui.setDB1, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setDB2, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setSegmentLength, "border",
                        "2px solid transparent")
    common.update_style(self.ui.setFetchSize, "border",
                        "2px solid transparent")
    common.update_style(self.ui.load_pages.row_3_groupbox, "border",
                        "2px solid transparent")
    common.update_style(self.ui.load_pages.row_3_groupbox, "border",
                        f"""2px solid {
                            self.themes["app_color"]["grey"]
                        }""")


def db_compare(self):
    """
    Control the input data for database comparison
    """
    init_db_compare(self)
    error = False

    if not self.ui.setDB1.currentText():
        common.update_style(self.ui.setDB1, "border", "2px solid red")
        error = True
    else:
        try:
            if not self.settings_db1[1].get("password"):
                common.update_style(self.ui.setDB1, "border", "2px solid red")
                error = True
                self.ui.setDB1.setCurrentIndex(-1)
                self.settings_db1 = None
        except (KeyError, TypeError):
            pass

    if not self.ui.setDB2.currentText():
        common.update_style(self.ui.setDB2, "border", "2px solid red")
        error = True
    else:
        try:
            if not self.settings_db2[1].get("password"):
                common.update_style(self.ui.setDB2, "border", "2px solid red")
                error = True
                self.ui.setDB2.setCurrentIndex(-1)
                self.settings_db2 = None
        except (KeyError, TypeError):
            pass

    if not self.ui.hashmode.isChecked() and \
            not self.ui.linemode.isChecked() and \
            not self.ui.columnmode.isChecked():
        common.update_style(self.ui.load_pages.row_3_groupbox,
                            "border", "2px solid red")

        error = True

    if self.ui.setExtractionType.isChecked() and\
            self.ui.setSegmentLength.text() in ["0", ""]:
        common.update_style(self.ui.setSegmentLength,
                            "border", "2px solid red")
        error = True

    if self.ui.setFetchSize.text() in ["0", ""]:
        common.update_style(self.ui.setFetchSize,
                            "border", "2px solid red")
        error = True

    if not error:
        self.ui.compare.setEnabled(True)
        return

    texte = QtCore.QCoreApplication.translate(
        "exceptions", "Correct errors")
    self.ui.logbar.log_label.setText(texte)

    common.update_style(self.ui.logbar.log_label, "color", "red")
