# -*- coding: utf-8 -*-

"""
Module: events
Auteur: creagleone
Date: 2025-05-07

Description:
    This module contains functions to manage events handler

Dépendances:
    - ast
    - time
    - QtWidgets (PySide6)
    - QtGui (PySide6)
    - QtCore (PySide6)
    - popups.py
    - controls.py
    - functions.py
    - themes.py
    - config.py
    - exceptions.py
    - orders.py
    - common.py
    - oracle.py

Usage Example:
    - N/A

Notes:
    - N/A
"""

import ast
import time
from PySide6 import QtWidgets, QtGui, QtCore
from gui.views import popups, controls
from gui.core import functions, themes
from core.utils import config, exceptions, orders, common
from core.database import oracle


class KeyEventFilter(QtWidgets.QWidget):
    key_pressed = QtCore.Signal(QtCore.QEvent)

    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            self.key_pressed.emit(event)
            return True
        return super(KeyEventFilter, self).eventFilter(source, event)


class MainEventHandler():
    def __init__(self, root):
        self.root = root
        self.ui = root.ui
        self.settings_db1 = []
        self.settings_db2 = []
        self.use_segments = False
        self.worker = None

        self.current_editable_row = -1
        self.tables_list = []

        self.current_choice = None
        self.db_query = None
        self.config_list = None
        self.update_db_list()

        self.ui.left_column.clicked.connect(self.root.btn_clicked)
        self.ui.title_bar.clicked.connect(self.root.btn_clicked)
        self.ui.left_menu.clicked.connect(self.root.btn_clicked)

        self.themes = themes.Themes().get_theme()

        self.ui.setDB1.activated.connect(
            lambda: self.on_db_changed("db1"))
        self.ui.setDB2.activated.connect(lambda: self.on_db_changed("db2"))
        self.ui.compare.setEnabled(False)
        self.ui.compare.clicked.connect(lambda: controls.db_compare(self))
        self.ui.compare.clicked.connect(self.execute_order_66)

        self.ui.setDB1.activated.connect(lambda: controls.db_compare(self))
        self.ui.setDB2.activated.connect(lambda: controls.db_compare(self))
        self.ui.setExtractionType.stateChanged.connect(
            lambda: controls.db_compare(self))

        self.ui.right_btn1.clicked.connect(
            lambda:
            functions.set_right_column_menu(
                self.ui,
                self.ui.right_column.menu_2
            ))

        self.ui.right_btn2.clicked.connect(
            lambda:
            functions.set_right_column_menu(
                self.ui,
                self.ui.right_column.menu_1
            ))

        self.ui.setSegmentLength.textChanged.connect(
            lambda: controls.db_compare(self))
        self.ui.setFetchSize.textChanged.connect(
            lambda: controls.db_compare(self))

        self.ui.hashmode.toggled.connect(lambda: controls.db_compare(self))
        self.ui.linemode.toggled.connect(lambda: controls.db_compare(self))
        self.ui.columnmode.toggled.connect(lambda: controls.db_compare(self))

        self.ui.oracle_selector.clicked.connect(self.oracle_view)

        self.ui.setExtractionType.stateChanged.connect(self.handle_toggle)

        validator = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression(r"\d{1,9}(\s\d{3})*"))

        self.ui.setSegmentLength.setValidator(validator)
        self.ui.setFetchSize.setValidator(validator)

        self.ui.clearDB.clicked.connect(self.clear_db)
        self.ui.saveDB.clicked.connect(self.save_db)

        self.ui.clear_data.clicked.connect(self.clear_data)

        self.ui.setSIDOracle.activated.connect(
            lambda: controls.oracle(self))

        self.ui.setHostOracle.textChanged.connect(
            lambda: controls.oracle(self))
        self.ui.setPortOracle.textChanged.connect(
            lambda: controls.oracle(self))
        self.ui.setDBOracle.textChanged.connect(
            lambda: controls.oracle(self))
        self.ui.setUsernameOracle.textChanged.connect(
            lambda: controls.oracle(self))
        self.ui.setPasswordOracle.textChanged.connect(
            lambda: controls.oracle(self))
        self.ui.setCustomName.textChanged.connect(
            lambda: controls.oracle(self))

        self.ui.tableWidget.cellClicked.connect(self.on_cell_clicked)
        self.key_event_filter = KeyEventFilter(self.ui.tableWidget)
        self.key_event_filter.key_pressed.connect(self.handle_key_press)
        self.ui.tableWidget.installEventFilter(self.key_event_filter)
        self.ui.select_all.clicked.connect(self.add_all_table)
        self.ui.unselect_all.clicked.connect(self.ignore_all_table)

        self.ui.testDB.clicked.connect(self.test_db)

    def on_cell_clicked(self, row, column):
        self.current_editable_row = row

    def handle_key_press(self, event):
        if self.ui.tableWidget.hasFocus():
            if event.key() == QtCore.Qt.Key_Delete:
                text = QtCore.QCoreApplication.translate(
                    "events", "Ignore")
                if self.ui.tableWidget.item(
                        self.current_editable_row, 0).text() != text:
                    self.ui.tableWidget.setItem(
                        self.current_editable_row, 0,
                        QtWidgets.QTableWidgetItem(text))
                    self.tables_list.remove(
                        self.ui.tableWidget.item(self.current_editable_row,
                                                 1).text())
            elif event.key() == QtCore.Qt.Key_Backspace:
                text = QtCore.QCoreApplication.translate(
                    "events", "Compare")
                if self.ui.tableWidget.item(
                        self.current_editable_row, 0).text() != text:
                    self.ui.tableWidget.setItem(
                        self.current_editable_row, 0,
                        QtWidgets.QTableWidgetItem(text))
                    self.tables_list.append(
                        self.ui.tableWidget.item(self.current_editable_row,
                                                 1).text())
        return

    def add_all_table(self):
        self.tables_list = []
        text = QtCore.QCoreApplication.translate(
            "events", "Compare")
        for row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.setItem(
                row, 0, QtWidgets.QTableWidgetItem(text))
            self.tables_list.append(self.ui.tableWidget.item(row, 1).text())
        return

    def ignore_all_table(self):
        self.tables_list = []
        text = QtCore.QCoreApplication.translate(
            "events", "Ignore")
        for row in range(self.ui.tableWidget.rowCount()):
            self.ui.tableWidget.setItem(
                row, 0, QtWidgets.QTableWidgetItem(text))

    def update_db_list(self):
        self.db_query = "SELECT nom, connexion_type, settings FROM db_config"
        self.config_list = config.get_list_data(self.db_query)
        self.ui.setDB1.clear()
        self.ui.setDB2.clear()

        self.ui.setDB1.addItems([row[0] for row in self.config_list])
        self.ui.setDB2.addItems([row[0] for row in self.config_list])
        self.ui.setDB1.setCurrentIndex(-1)
        self.ui.setDB2.setCurrentIndex(-1)

    def clear_data(self):
        self.ui.setDB1.blockSignals(True)
        self.ui.setDB2.blockSignals(True)
        self.ui.setExtractionType.blockSignals(True)
        self.ui.setSegmentLength.blockSignals(True)
        self.ui.setFetchSize.blockSignals(True)

        self.ui.tableWidget.setRowCount(0)
        self.tables_list = []
        self.current_editable_row = -1
        self.ui.setDB1.setCurrentIndex(-1)
        self.ui.setDB2.setCurrentIndex(-1)
        self.ui.setExtractionType.setChecked(False)
        self.ui.setExtractionType.setup_animation(0)
        self.ui.setSegmentLength.setText("")
        self.ui.setFetchSize.setText("")

        for btn in self.ui.load_pages.contents.findChildren(
                QtWidgets.QRadioButton):
            btn.blockSignals(True)
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)
            btn.blockSignals(False)

        self.ui.setDB1.blockSignals(False)
        self.ui.setDB2.blockSignals(False)
        self.ui.setExtractionType.blockSignals(False)
        self.ui.setSegmentLength.blockSignals(False)
        self.ui.setFetchSize.blockSignals(False)

        controls.init_db_compare(self)

    def test_db(self):
        """
        Test the connection to a database
        """
        self.ui.testDB.setEnabled(False)
        self.ui.clearDB.setEnabled(False)
        self.ui.saveDB.setEnabled(False)
        settings = {}
        if self.current_choice == "Oracle":
            settings = {
                "host": self.ui.setHostOracle.text(),
                "port": self.ui.setPortOracle.text(),
                "dsn": self.ui.setDBOracle.text(),
                "dsn_type": self.ui.setSIDOracle.currentText(),
                "username": self.ui.setUsernameOracle.text(),
                "password": self.ui.setPasswordOracle.text()
            }
        self.worker = TestThread(settings)
        self.worker.signal_update.connect(self.popup)
        self.worker.signal_update.connect(
            lambda: self.ui.testDB.setEnabled(True))
        self.worker.signal_update.connect(
            lambda: self.ui.clearDB.setEnabled(True))
        self.worker.signal_update.connect(
            lambda: self.ui.saveDB.setEnabled(True))
        self.worker.start()

    def save_db(self):
        """
        Save database config
        """
        settings = {}
        if self.current_choice == "Oracle":
            settings = {
                "host": self.ui.setHostOracle.text(),
                "port": self.ui.setPortOracle.text(),
                "dsn": self.ui.setDBOracle.text(),
                "dsn_type": self.ui.setSIDOracle.currentText(),
                "username": self.ui.setUsernameOracle.text(),
                "password": self.ui.setPasswordOracle.text()
                if self.ui.isSavePwdOracle.isChecked() else ""
            }
        query = '''INSERT INTO db_config (nom, connexion_type,
        settings, date_creation) VALUES (?,?,?,?)'''
        args = (
            self.ui.setCustomName.text(), self.current_choice,
            str(settings)
        )
        try:
            config.insert_query_db(query=query, args=args)

        except exceptions.Error as e:
            # TODO: FIX that
            TestThread.signal_update.emit("error", e.message)
        popups.display_info(exceptions.MESSAGES.get(100))

        self.update_db_list()
        self.clear_db()

    def clear_db(self):
        """
        Clear all fields of compare databases
        """
        self.current_choice = None
        self.ui.load_pages.settings.hide()
        self.clear_oracle_data()
        controls.init_oracle(self)

    def clear_oracle_data(self):
        """
        Clear all fields of oracle config
        """
        self.ui.load_pages.oracle.hide()
        self.ui.isSavePwdOracle.setChecked(False)

        self.ui.setHostOracle.blockSignals(True)
        self.ui.setPortOracle.blockSignals(True)
        self.ui.setDBOracle.blockSignals(True)
        self.ui.setSIDOracle.blockSignals(True)
        self.ui.setUsernameOracle.blockSignals(True)
        self.ui.setUsernameOracle.blockSignals(True)
        self.ui.setCustomName.blockSignals(True)

        self.ui.setHostOracle.setText("")
        self.ui.setPortOracle.setText("1521")
        self.ui.setDBOracle.setText("")
        self.ui.setSIDOracle.setCurrentIndex(0)
        self.ui.setUsernameOracle.setText("")
        self.ui.setPasswordOracle.setText("")
        self.ui.setCustomName.setText("")

        for btn in self.ui.load_pages.contents_2.findChildren(
                QtWidgets.QToolButton):
            btn.blockSignals(True)
            btn.setAutoExclusive(False)
            btn.setChecked(False)
            btn.setAutoExclusive(True)
            btn.blockSignals(False)

        self.ui.setHostOracle.blockSignals(False)
        self.ui.setPortOracle.blockSignals(False)
        self.ui.setDBOracle.blockSignals(False)
        self.ui.setSIDOracle.blockSignals(False)
        self.ui.setUsernameOracle.blockSignals(False)
        self.ui.setUsernameOracle.blockSignals(False)
        self.ui.setCustomName.blockSignals(False)

    def oracle_view(self):
        self.ui.load_pages.oracle.show()
        self.ui.load_pages.settings.show()
        self.current_choice = "Oracle"

    def handle_toggle(self, state):
        if state == 2:
            self.ui.setSegmentLength.setEnabled(True)
        else:
            self.ui.setSegmentLength.setEnabled(False)

    def on_db_changed(self, db):
        title = QtCore.QCoreApplication.translate(
            "events", "Input password")
        message = QtCore.QCoreApplication.translate(
            "events", "To continue, enter the password :")
        if db == "db1":
            self.settings_db1 = next(
                ([db_type, ast.literal_eval(settings),
                  self.ui.setDB1.currentText()]
                 for key, db_type, settings in self.config_list
                 if key == self.ui.setDB1.currentText()), None)

            if not self.settings_db1[1].get("password"):
                password = popups.input_value(title, message)
                if password:
                    self.settings_db1[1]["password"] = password
        elif db == "db2":
            self.settings_db2 = next(
                ([db_type, ast.literal_eval(settings),
                  self.ui.setDB2.currentText()]
                 for key, db_type, settings in self.config_list
                 if key == self.ui.setDB2.currentText()), None)

            if not self.settings_db2[1].get("password"):
                password = popups.input_value(title, message)
                if password:
                    self.settings_db2[1]["password"] = password

        if self.settings_db1 and self.settings_db2:
            self.tables_list = []
            self.worker = FiltersTablesThread(
                self.settings_db1, self.settings_db2,
                self.ui, self.tables_list)
            self.worker.signal_update.connect(
                self.popup)
            self.worker.start()

    def execute_order_66(self):
        self.ui.compare.setEnabled(False)
        self.ui.clear_data.setEnabled(False)
        text = QtCore.QCoreApplication.translate("events",
                                                 "Processing in progress...")
        self.ui.logbar.log_label.setText(text)
        common.update_style(self.ui.logbar.log_label, "color",
                            self.themes["app_color"]["text_infos"])

        segment_length = int(self.ui.setSegmentLength.text(
        )) if self.ui.setExtractionType.isChecked() else None

        if self.ui.hashmode.isChecked():
            mode = "hash"
        elif self.ui.linemode.isChecked():
            mode = "line"
        else:
            mode = "column"

        self.worker = WorkerThread(mode, self.settings_db1, self.settings_db2,
                                   segment_length, self.tables_list,
                                   int(self.ui.setFetchSize.text()))

        self.worker.signal_update.connect(
            self.popup)
        self.worker.signal_update.connect(
            lambda: self.ui.compare.setEnabled(True))
        self.worker.signal_update.connect(
            lambda: self.ui.clear_data.setEnabled(True))
        self.worker.start()

    def popup(self, display_type, text):
        log = QtCore.QCoreApplication.translate("events",
                                                "End of treatment")
        self.ui.logbar.log_label.setText(log)

        if display_type == "error":
            popups.display_error(text)
        elif display_type == "warn":
            if self.ui.hashmode.isChecked():
                popups.display_warn(text, False)
            else:
                rtn = popups.display_warn(text)
                if rtn:
                    folder_path = common.get_work_folder("gap")
                    common.open_folders(folder_path)
        else:
            popups.display_info(text)
        self.ui.logbar.log_label.setText("")
        common.update_style(self.ui.logbar.log_label, "color",
                            self.themes["app_color"]["text_description"])


class TestThread(QtCore.QThread):
    signal_update = QtCore.Signal(str, str)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def run(self):
        try:
            query = "SELECT banner FROM v$version"
            start_time = time.time()
            content = oracle.get_unique_data(self.settings, query=query)
            ping_time = (time.time() - start_time) * 1000

            text = f"""Server : {content} \n
            Ping response time : {ping_time:.2f} ms"""

            message = QtCore.QCoreApplication.translate(
                "exceptions", text)

        except exceptions.Error as e:
            self.signal_update.emit("error", e.message)
        else:
            self.signal_update.emit("info", message)


class FiltersTablesThread(QtCore.QThread):
    signal_update = QtCore.Signal(str, str)
    # show_signal = QtCore.Signal()

    def __init__(self, settings_db1, settings_db2, content, table_list):
        super().__init__()
        self.settings_db1 = settings_db1
        self.settings_db2 = settings_db2
        self.content = content
        self.tables_list = table_list

        self.signal_update.connect(self.show_error)

    def show_error(self):
        self.content.tableWidget.setRowCount(0)
        self.content.tableWidget.setRowCount(1)
        text = QtCore.QCoreApplication.translate(
            "events", "Unable to retrieve common tables")
        item = QtWidgets.QTableWidgetItem(text)
        item.setFont(QtGui.QFont("Arial", 20, QtGui.QFont.Bold))
        item.setForeground(QtGui.QColor(255, 0, 0))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.content.tableWidget.setSpan(0, 0, 1,
                                         self.content.tableWidget.columnCount()
                                         )
        self.content.tableWidget.setItem(0, 0, item)

    def run(self):
        try:
            self.content.tableWidget.setRowCount(0)
            data = common.get_common_tables(
                self.settings_db1, self.settings_db2)
            self.content.tableWidget.setRowCount(len(data))
            for row_idx, (key, values) in enumerate(data.items()):
                text = QtCore.QCoreApplication.translate(
                    "events", "Compare")
                self.content.tableWidget.setItem(
                    row_idx, 0, QtWidgets.QTableWidgetItem(text))
                self.content.tableWidget.setItem(
                    row_idx, 1, QtWidgets.QTableWidgetItem(key))
                self.tables_list.append(key)

                for col_idx, value in enumerate(values):
                    self.content.tableWidget.setItem(
                        row_idx, col_idx + 2,
                        QtWidgets.QTableWidgetItem(str(value)))

        except exceptions.Error as e:
            # self.show_error()
            self.signal_update.emit("error", e.message)
        # else:
        #     self.show_signal.emit()


class WorkerThread(QtCore.QThread):
    signal_update = QtCore.Signal(str, str)

    def __init__(self, mode, settings_db1, settings_db2, segment,
                 compare_tables, fetch):
        super().__init__()
        self.mode = mode
        self.settings_db1 = settings_db1
        self.settings_db2 = settings_db2
        self.segment = segment
        self.compare_tables = compare_tables
        self.fetch = fetch

    def run(self):
        try:
            resultat = orders.compare_db(self.mode, self.settings_db1,
                                         self.settings_db2,
                                         self.segment,
                                         self.compare_tables,
                                         self.fetch)
        except exceptions.Error as e:
            self.signal_update.emit("error", e.message)
        except exceptions.Warn as e:
            self.signal_update.emit("warn", e.message)
        else:
            message = exceptions.MESSAGES.get(
                int(resultat),
                QtCore.QCoreApplication.translate(
                    "exceptions", "Unknown code"))
            self.signal_update.emit("info", message)
