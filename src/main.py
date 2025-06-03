# -*- coding: utf-8 -*-

import sys
import os
import traceback
import types
from PySide6 import QtWidgets, QtCore, QtGui
from gui.core import functions
from gui.views import ui_main, events
from core.utils import config, exceptions, common, logs


class MainWindow(QtWidgets.QMainWindow):
    error_signal = QtCore.Signal(tuple)

    def __init__(self):
        super().__init__()
        self.ui = ui_main.UI_MainWindow(self)
        self.main_event = events.MainEventHandler(self)

    def btn_clicked(self):
        btn = self.setup_btns()

        if btn.objectName() != "btn_settings":
            self.ui.left_menu.deselect_all_tab()

        top_settings = functions.get_title_bar_btn(
            self.ui, "btn_top_settings")
        top_settings.set_active(False)

        if btn.objectName() == "btn_home":
            self.ui.left_menu.select_only_one(btn.objectName())
            functions.set_page(self.ui, self.ui.load_pages.page_1)

        if btn.objectName() == "btn_compare":
            self.ui.left_menu.select_only_one(btn.objectName())
            functions.set_page(self.ui, self.ui.load_pages.page_2)

        if btn.objectName() == "btn_add_connection":
            self.ui.left_menu.select_only_one(btn.objectName())
            functions.set_page(self.ui, self.ui.load_pages.page_3)

        if btn.objectName() == "btn_info":
            if not functions.left_column_is_visible(self.ui):
                self.ui.left_menu.select_only_one_tab(btn.objectName())
                functions.toggle_left_column(self.ui)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    functions.toggle_left_column(self.ui)

                self.ui.left_menu.select_only_one_tab(btn.objectName())

            if btn.objectName() != "btn_close_left_column":
                functions.set_left_column_menu(
                    self.ui,
                    menu=self.ui.left_column.menus.menu_2,
                    title="Info tab",
                    icon_path=common.set_svg_icon("icon_info.svg")
                )

        if btn.objectName() == "btn_settings" or \
                btn.objectName() == "btn_close_left_column":
            if not functions.left_column_is_visible(self.ui):
                functions.toggle_left_column(self.ui)
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    functions.toggle_left_column(self.ui)
                self.ui.left_menu.select_only_one_tab(btn.objectName())

            if btn.objectName() != "btn_close_left_column":
                functions.set_left_column_menu(
                    self.ui,
                    menu=self.ui.left_column.menus.menu_1,
                    title="Settings Left Column",
                    icon_path=common.set_svg_icon(
                        "icon_settings.svg")
                )

        if btn.objectName() == "btn_top_settings":
            if not functions.right_column_is_visible(self.ui):
                btn.set_active(True)
                functions.toggle_right_column(self.ui)
            else:
                btn.set_active(False)
                functions.toggle_right_column(self.ui)

            top_settings = functions.get_left_menu_btn(
                self.ui, "btn_settings")
            top_settings.set_active_tab(False)

    def setup_btns(self):
        if self.ui.title_bar.sender():
            return self.ui.title_bar.sender()
        if self.ui.left_menu.sender():
            return self.ui.left_menu.sender()
        if self.ui.left_column.sender():
            return self.ui.left_column.sender()

    def resizeEvent(self, event):
        self.ui.resize_grips()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()


def exception_hook(exctype: type[BaseException],
                   value: BaseException,
                   tb: types.TracebackType) -> None:
    """
    Custom exception hook to log errors

    Args:
        exctype (type[BaseException]): Exception type
        value (BaseException): Exception value
        tb (traceback.TracebackType): Exception traceback
    """
    error_message = "".join(traceback.format_exception(exctype, value, tb))
    logs.log_critical(error_message)
    exceptions.ErrorSignal(exceptions.Error(999))


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.ico"))
    screen = app.primaryScreen()
    screen_size = screen.size()

    if screen_size.width() >= 3840 and screen_size.height() >= 2160:
        os.environ["QT_SCALE_FACTOR"] = "2"

    os.environ["QT_FONT_DPI"] = "96"

    try:
        config.setup_db()
    except exceptions.Error:
        sys.exit(0)

    translator = QtCore.QTranslator()
    locale = common.get_current_locale()

    file = common.set_locale(locale + ".qm")

    translator.load(file)
    app.installTranslator(translator)

    logs.log_config()
    window = MainWindow()
    window.show()

    sys.excepthook = exception_hook

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
