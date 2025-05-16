# -*- coding: utf-8 -*-

from PySide6 import QtCore, QtWidgets, QtSvgWidgets
from gui.widgets import (py_window, py_left_menu, py_left_column,
                         py_title_bar, py_logbar, py_grips, py_push_button,
                         py_line_edit, py_toggle, py_combobox, py_radio_button,
                         py_label, py_tool_button)
from gui.views import ui_main_pages, ui_right_column
from gui.core import functions, settings, themes
from core.utils import common


class UI_MainWindow(object):
    add_left_menus = [
        {
            "btn_icon": "icon_home.svg",
            "btn_id": "btn_home",
            "btn_text": "Home",
            "btn_tooltip": "Home page",
            "show_top": True,
            "is_active": True
        },
        {
            "btn_icon": "icon_widgets.svg",
            "btn_id": "btn_widgets",
            "btn_text": "Compare database",
            "btn_tooltip": "Compare database",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_add_user.svg",
            "btn_id": "btn_add_user",
            "btn_text": "Add a new config",
            "btn_tooltip": "Add DB config",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_info.svg",
            "btn_id": "btn_info",
            "btn_text": "Information",
            "btn_tooltip": "Open informations",
            "show_top": False,
            "is_active": False
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_settings",
            "btn_text": "Settings",
            "btn_tooltip": "Open settings",
            "show_top": False,
            "is_active": False
        }
    ]

    add_title_bar_menus = [
        {
            "btn_icon": "icon_search.svg",
            "btn_id": "btn_search",
            "btn_tooltip": "Search",
            "is_active": False
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_top_settings",
            "btn_tooltip": "Top settings",
            "is_active": False
        }
    ]

    def __init__(self, parent):
        self.settings = settings.Settings().get_settings()
        self.themes = themes.Themes().get_theme()
        self.parent = parent

        self.setup_ui()
        self.setup_gui()

        self.setup_page2()
        self.setup_page3()
        self.settings_left_column()
        self.settings_right_column()
        self.settings_oracle()
        self.settings_DB_buttons()

    def setup_ui(self):
        if not self.parent.objectName():
            self.parent.setObjectName("MainWindow")

        self.parent.resize(self.settings["startup_size"]
                           [0], self.settings["startup_size"][1])
        self.parent.setMinimumSize(
            self.settings["minimum_size"][0], self.settings["minimum_size"][1])

        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setStyleSheet(f'''
            font: {
            self.settings["font"]["text_size"]}pt
                "{self.settings["font"]["family"]}";
            color: {self.themes["app_color"]["text_foreground"]};
        ''')
        self.central_widget_layout = QtWidgets.QVBoxLayout(self.central_widget)
        if self.settings["custom_title_bar"]:
            self.central_widget_layout.setContentsMargins(10, 10, 10, 10)
        else:
            self.central_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.window = py_window.PyWindow(
            self.parent,
            bg_color=self.themes["app_color"]["bg_one"],
            border_color=self.themes["app_color"]["bg_two"],
            text_color=self.themes["app_color"]["text_foreground"]
        )

        if not self.settings["custom_title_bar"]:
            self.window.set_stylesheet(border_radius=0, border_size=0)

        self.central_widget_layout.addWidget(self.window)

        left_menu_margin = self.settings["left_menu_content_margins"]
        left_menu_minimum = self.settings["lef_menu_size"]["minimum"]
        self.left_menu_frame = QtWidgets.QFrame()
        self.left_menu_frame.setMaximumSize(
            left_menu_minimum + (left_menu_margin * 2), 17280)
        self.left_menu_frame.setMinimumSize(
            left_menu_minimum + (left_menu_margin * 2), 0)

        self.left_menu_layout = QtWidgets.QHBoxLayout(self.left_menu_frame)
        self.left_menu_layout.setContentsMargins(
            left_menu_margin,
            left_menu_margin,
            left_menu_margin,
            left_menu_margin
        )

        self.left_menu = py_left_menu.PyLeftMenu(
            parent=self.left_menu_frame,
            app_parent=self.central_widget,
            dark_one=self.themes["app_color"]["dark_one"],
            dark_three=self.themes["app_color"]["dark_three"],
            dark_four=self.themes["app_color"]["dark_four"],
            bg_one=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            context_color=self.themes["app_color"]["context_color"],
            text_foreground=self.themes["app_color"]["text_foreground"],
            text_active=self.themes["app_color"]["text_active"]
        )
        self.left_menu_layout.addWidget(self.left_menu)

        self.left_column_frame = QtWidgets.QFrame()
        self.left_column_frame.setMaximumWidth(
            self.settings["left_column_size"]["minimum"])
        self.left_column_frame.setMinimumWidth(
            self.settings["left_column_size"]["minimum"])
        self.left_column_frame.setStyleSheet(
            f"background: {self.themes['app_color']['bg_two']}")

        self.left_column_layout = QtWidgets.QVBoxLayout(self.left_column_frame)
        self.left_column_layout.setContentsMargins(0, 0, 0, 0)

        self.left_column = py_left_column.PyLeftColumn(
            self.parent,
            app_parent=self.central_widget,
            text_title="Settings Left Frame",
            text_title_size=self.settings["font"]["title_size"],
            text_title_color=self.themes['app_color']['text_foreground'],
            icon_path=common.set_svg_icon("icon_settings.svg"),
            dark_one=self.themes['app_color']['dark_one'],
            bg_color=self.themes['app_color']['bg_three'],
            btn_color=self.themes['app_color']['bg_three'],
            btn_color_hover=self.themes['app_color']['bg_two'],
            btn_color_pressed=self.themes['app_color']['bg_one'],
            icon_color=self.themes['app_color']['icon_color'],
            icon_color_hover=self.themes['app_color']['icon_hover'],
            context_color=self.themes['app_color']['context_color'],
            icon_color_pressed=self.themes['app_color']['icon_pressed'],
            icon_close_path=common.set_svg_icon("icon_close.svg")
        )
        self.left_column_layout.addWidget(self.left_column)

        self.right_app_frame = QtWidgets.QFrame()

        self.right_app_layout = QtWidgets.QVBoxLayout(self.right_app_frame)
        self.right_app_layout.setContentsMargins(3, 3, 3, 3)
        self.right_app_layout.setSpacing(6)

        self.title_bar_frame = QtWidgets.QFrame()
        self.title_bar_frame.setMinimumHeight(40)
        self.title_bar_frame.setMaximumHeight(40)
        self.title_bar_layout = QtWidgets.QVBoxLayout(self.title_bar_frame)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = py_title_bar.PyTitleBar(
            self.parent,
            logo_width=40,
            app_parent=self.central_widget,
            logo_image="logo.svg",
            bg_color=self.themes["app_color"]["bg_two"],
            div_color=self.themes["app_color"]["bg_three"],
            btn_bg_color=self.themes["app_color"]["bg_two"],
            btn_bg_color_hover=self.themes["app_color"]["bg_three"],
            btn_bg_color_pressed=self.themes["app_color"]["bg_one"],
            icon_color=self.themes["app_color"]["icon_color"],
            icon_color_hover=self.themes["app_color"]["icon_hover"],
            icon_color_pressed=self.themes["app_color"]["icon_pressed"],
            icon_color_active=self.themes["app_color"]["icon_active"],
            context_color=self.themes["app_color"]["context_color"],
            dark_one=self.themes["app_color"]["dark_one"],
            text_foreground=self.themes["app_color"]["text_foreground"],
            radius=8,
            font_family=self.settings["font"]["family"],
            title_size=self.settings["font"]["title_size"],
            is_custom_title_bar=self.settings["custom_title_bar"]
        )
        self.title_bar_layout.addWidget(self.title_bar)

        self.content_area_frame = QtWidgets.QFrame()

        self.content_area_layout = QtWidgets.QHBoxLayout(
            self.content_area_frame)
        self.content_area_layout.setContentsMargins(0, 0, 0, 0)
        self.content_area_layout.setSpacing(0)

        self.content_area_left_frame = QtWidgets.QFrame()

        self.load_pages = ui_main_pages.Ui_MainPages()
        self.load_pages.setupUi(self.content_area_left_frame)

        self.right_column_frame = QtWidgets.QFrame()
        self.right_column_frame.setMinimumWidth(
            self.settings["right_column_size"]["minimum"])
        self.right_column_frame.setMaximumWidth(
            self.settings["right_column_size"]["minimum"])

        self.content_area_right_layout = QtWidgets.QVBoxLayout(
            self.right_column_frame)
        self.content_area_right_layout.setContentsMargins(5, 5, 5, 5)
        self.content_area_right_layout.setSpacing(0)

        self.content_area_right_bg_frame = QtWidgets.QFrame()
        self.content_area_right_bg_frame.setObjectName(
            "content_area_right_bg_frame")
        self.content_area_right_bg_frame.setStyleSheet(f'''
        #content_area_right_bg_frame {{
            border-radius: 8px;
            background-color: {self.themes["app_color"]["bg_two"]};
        }}
        ''')

        self.content_area_right_layout.addWidget(
            self.content_area_right_bg_frame)

        self.right_column = ui_right_column.Ui_RightColumn()
        self.right_column.setupUi(self.content_area_right_bg_frame)

        self.content_area_layout.addWidget(self.content_area_left_frame)
        self.content_area_layout.addWidget(self.right_column_frame)

        self.logbar_frame = QtWidgets.QFrame()
        self.logbar_frame.setMinimumHeight(26)
        self.logbar_frame.setMaximumHeight(26)

        self.logbar_layout = QtWidgets.QVBoxLayout(self.logbar_frame)
        self.logbar_layout.setContentsMargins(0, 0, 0, 0)

        self.logbar = py_logbar.PyLogBar(
            bg_two=self.themes["app_color"]["bg_two"],
            copyright=self.settings["copyright"],
            version=self.settings["version"],
            font_family=self.settings["font"]["family"],
            text_size=self.settings["font"]["text_size"],
            text_description_color=self.themes["app_color"]["text_description"]
        )

        self.logbar_layout.addWidget(self.logbar)

        self.right_app_layout.addWidget(self.title_bar_frame)
        self.right_app_layout.addWidget(self.content_area_frame)
        self.right_app_layout.addWidget(self.logbar_frame)

        self.window.layout.addWidget(self.left_menu_frame)
        self.window.layout.addWidget(self.left_column_frame)
        self.window.layout.addWidget(self.right_app_frame)

        self.parent.setCentralWidget(self.central_widget)

    def setup_gui(self):
        self.hide_grips = True
        self.parent.setWindowTitle(self.settings["app_name"])
        if self.settings["custom_title_bar"]:
            self.parent.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            self.parent.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        if self.settings["custom_title_bar"]:
            self.left_grip = py_grips.PyGrips(
                self.parent, "left", self.hide_grips)
            self.right_grip = py_grips.PyGrips(
                self.parent, "right", self.hide_grips)
            self.top_grip = py_grips.PyGrips(
                self.parent, "top", self.hide_grips)
            self.bottom_grip = py_grips.PyGrips(
                self.parent, "bottom", self.hide_grips)
            self.top_left_grip = py_grips.PyGrips(
                self.parent, "top_left", self.hide_grips)
            self.top_right_grip = py_grips.PyGrips(
                self.parent, "top_right", self.hide_grips)
            self.bottom_left_grip = py_grips.PyGrips(
                self.parent, "bottom_left", self.hide_grips)
            self.bottom_right_grip = py_grips.PyGrips(
                self.parent, "bottom_right", self.hide_grips)

        self.left_menu.add_menus(self.add_left_menus)
        self.title_bar.add_menus(self.add_title_bar_menus)

        if self.settings["custom_title_bar"]:
            self.title_bar.set_title(self.settings["app_name"])
        else:
            self.title_bar.set_title("Dbtective Compare Tool")

        functions.set_page(
            self, self.load_pages.page_1)
        functions.set_left_column_menu(
            self,
            menu=self.left_column.menus.menu_1,
            title="Settings Left Column",
            icon_path=common.set_svg_icon("icon_settings.svg")
        )
        functions.set_right_column_menu(
            self, self.right_column.menu_1)

        self.logo_svg = QtSvgWidgets.QSvgWidget(
            common.set_svg_image("logo.svg"))
        self.logo_svg.setFixedSize(100, 100)
        self.load_pages.logo_layout.addWidget(
            self.logo_svg, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)

    def setup_page2(self):
        self.label_db1 = py_label.PyLabel(
            text="Database 1",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.label_db1.setMinimumHeight(40)
        self.label_db1.setMaximumHeight(40)
        self.label_db1.setMinimumWidth(200)
        self.label_db1.setMaximumWidth(200)

        self.setDB1 = py_combobox.PyComboBox(
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setDB1.setMinimumHeight(40)
        self.setDB1.setMaximumHeight(40)
        self.setDB1.setMinimumWidth(200)
        self.setDB1.setMaximumWidth(200)

        self.label_db2 = py_label.PyLabel(
            text="Database 2",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.label_db2.setMinimumHeight(40)
        self.label_db2.setMaximumHeight(40)
        self.label_db2.setMinimumWidth(200)
        self.label_db2.setMaximumWidth(200)

        self.setDB2 = py_combobox.PyComboBox(
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setDB2.setMinimumHeight(40)
        self.setDB2.setMaximumHeight(40)
        self.setDB2.setMinimumWidth(200)
        self.setDB2.setMaximumWidth(200)

        self.label_extraction = py_label.PyLabel(
            text="Multiple queries",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.label_extraction.setMinimumHeight(40)
        self.label_extraction.setMaximumHeight(40)
        self.label_extraction.setMinimumWidth(200)
        self.label_extraction.setMaximumWidth(200)

        self.setExtractionType = py_toggle.PyToggle(
            width=50,
            bg_color=self.themes["app_color"]["dark_two"],
            circle_color=self.themes["app_color"]["icon_color"],
            active_color=self.themes["app_color"]["context_color"]
        )
        self.setExtractionType.setMinimumHeight(40)
        self.setExtractionType.setMaximumHeight(40)
        self.setExtractionType.setMinimumWidth(50)
        self.setExtractionType.setMaximumWidth(50)

        self.label_segment = py_label.PyLabel(
            text="Segment length",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.label_segment.setMinimumHeight(40)
        self.label_segment.setMaximumHeight(40)
        self.label_segment.setMinimumWidth(200)
        self.label_segment.setMaximumWidth(200)

        self.setSegmentLength = py_line_edit.PyLineEdit(
            text="",
            place_holder_text="setSegmentLength",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setSegmentLength.setMinimumHeight(40)
        self.setSegmentLength.setMaximumHeight(40)
        self.setSegmentLength.setMinimumWidth(200)
        self.setSegmentLength.setMaximumWidth(200)
        self.setSegmentLength.setDisabled(True)

        self.label_fetch = py_label.PyLabel(
            text="Fetch Size",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.label_fetch.setMinimumHeight(40)
        self.label_fetch.setMaximumHeight(40)
        self.label_fetch.setMinimumWidth(200)
        self.label_fetch.setMaximumWidth(200)

        self.setFetchSize = py_line_edit.PyLineEdit(
            text="",
            place_holder_text="setFetchSize",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setFetchSize.setMinimumHeight(40)
        self.setFetchSize.setMinimumWidth(200)
        self.setFetchSize.setMaximumWidth(200)

        self.hashmode = py_radio_button.PyRadioButton(
            text="Hash",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.hashmode.setMinimumHeight(40)
        self.hashmode.setMaximumHeight(40)
        self.hashmode.setMinimumWidth(200)
        self.hashmode.setMaximumWidth(200)

        self.fullmode = py_radio_button.PyRadioButton(
            text="Full",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.fullmode.setMinimumHeight(40)
        self.fullmode.setMaximumHeight(40)
        self.fullmode.setMinimumWidth(200)
        self.fullmode.setMaximumWidth(200)

        self.clear_data = py_push_button.PyPushButton(
            text="Clear",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            bg_color_disabled=self.themes["app_color"]["grey"],
            icon_path="icon_clear.svg"
        )
        self.clear_data.setMinimumHeight(40)
        self.clear_data.setMaximumHeight(40)
        self.clear_data.setMinimumWidth(150)
        self.clear_data.setMaximumWidth(150)

        self.compare = py_push_button.PyPushButton(
            text="Compare",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            bg_color_disabled=self.themes["app_color"]["grey"],
            icon_path="icon_compare.svg"
        )
        self.compare.setMinimumHeight(40)
        self.compare.setMaximumHeight(40)
        self.compare.setMinimumWidth(150)
        self.compare.setMaximumWidth(150)

        self.load_pages.db1.addWidget(self.label_db1)
        self.load_pages.db2.addWidget(self.label_db2)
        self.load_pages.db1.addWidget(self.setDB1)
        self.load_pages.db2.addWidget(self.setDB2)
        self.load_pages.row_2_groupbox.setStyleSheet(
            f"""border-radius: 8px;
            border: 2px solid {self.themes["app_color"]["grey"]};""")
        self.load_pages.row_3_groupbox.setStyleSheet(
            f"""border-radius: 8px;
            border: 2px solid {self.themes["app_color"]["grey"]};""")
        self.load_pages.extraction.addWidget(self.label_extraction, 0, 0)
        self.load_pages.extraction.addWidget(
            self.setExtractionType, 0, 1)
        self.load_pages.extraction.addWidget(self.label_segment, 1, 0)
        self.load_pages.extraction.addWidget(self.setSegmentLength, 1, 1)
        self.load_pages.extraction.addWidget(self.label_fetch, 2, 0)
        self.load_pages.extraction.addWidget(self.setFetchSize, 2, 1)
        self.load_pages.processing.addWidget(self.hashmode)
        self.load_pages.processing.addWidget(self.fullmode)
        self.load_pages.row_4_layout.setAlignment(QtCore.Qt.AlignRight)
        self.load_pages.row_4_layout.addWidget(self.clear_data)
        self.load_pages.row_4_layout.addWidget(self.compare)
        self.load_pages.description_label.setMaximumHeight(200)

    def setup_page3(self):
        self.load_pages.oracle.hide()
        self.load_pages.settings.hide()
        self.load_pages.title_label_2.setMaximumHeight(50)
        self.load_pages.description_label_2.setMaximumHeight(50)

        self.oracle_selector = py_tool_button.PyToolButton(
            text="Oracle",
            icon_path="oracle.svg",
            bg_color="transparent",
            border_size=0,
            bg_color_checked="#182ACC",
            bg_color_hover="#182ACC",
            is_checkable=True,
            is_autoexclusive=True

        )

        self.csv_selector = py_tool_button.PyToolButton(
            text="CSV (WIP)",
            icon_path="csv.svg",
            bg_color="transparent",
            border_size=0,
            bg_color_checked="#182ACC",
            bg_color_hover="#182ACC",
            is_checkable=True,
            is_autoexclusive=True,
            is_enabled=False

        )

        self.load_pages.DB_selector.addWidget(self.oracle_selector)
        self.load_pages.DB_selector.addWidget(self.csv_selector)

    def settings_oracle(self):
        self.labelHostOracle = py_label.PyLabel(
            text="Host",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.labelHostOracle.setMinimumHeight(40)
        self.labelHostOracle.setMaximumHeight(40)
        self.labelHostOracle.setMinimumWidth(200)
        self.labelHostOracle.setMaximumWidth(200)

        self.setHostOracle = py_line_edit.PyLineEdit(
            text="",
            place_holder_text="ip or address",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setHostOracle.setMinimumHeight(40)
        self.setHostOracle.setMaximumHeight(40)
        self.setHostOracle.setMinimumWidth(200)

        self.setPortOracle = py_line_edit.PyLineEdit(
            text="1521",
            place_holder_text="Port",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"],
            input_mask="9999"
        )
        self.setPortOracle.setMinimumHeight(40)
        self.setPortOracle.setMaximumHeight(40)
        self.setPortOracle.setMinimumWidth(100)
        self.setPortOracle.setMaximumWidth(100)

        self.labelDBOracle = py_label.PyLabel(
            text="Database",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.labelDBOracle.setMinimumHeight(40)
        self.labelDBOracle.setMaximumHeight(40)
        self.labelDBOracle.setMinimumWidth(200)
        self.labelDBOracle.setMaximumWidth(200)

        self.setDBOracle = py_line_edit.PyLineEdit(
            text="",
            place_holder_text="",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setDBOracle.setMinimumHeight(40)
        self.setDBOracle.setMaximumHeight(40)
        self.setDBOracle.setMinimumWidth(200)

        self.setSIDOracle = py_combobox.PyComboBox(
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setSIDOracle.setMinimumHeight(40)
        self.setSIDOracle.setMaximumHeight(40)
        self.setSIDOracle.setMinimumWidth(200)
        self.setSIDOracle.setMaximumWidth(200)
        self.setSIDOracle.addItems(["SID", "Service Name"])

        self.load_pages.settings_oracle.addWidget(
            self.labelHostOracle, 0, 0)
        self.load_pages.settings_oracle.addWidget(
            self.setHostOracle, 0, 1)
        self.load_pages.settings_oracle.addWidget(
            self.setPortOracle, 0, 2)
        self.load_pages.settings_oracle.addWidget(
            self.labelDBOracle, 1, 0)
        self.load_pages.settings_oracle.addWidget(self.setDBOracle, 1, 1)
        self.load_pages.settings_oracle.addWidget(
            self.setSIDOracle, 1, 2)

        self.labelAuthOracle = py_label.PyLabel(
            text="Authentification",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.labelAuthOracle.setMinimumHeight(40)
        self.labelAuthOracle.setMaximumHeight(40)
        self.labelAuthOracle.setMinimumWidth(200)
        self.labelAuthOracle.setMaximumWidth(200)

        self.setAuthentification = py_combobox.PyComboBox(
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setAuthentification.setMinimumHeight(40)
        self.setAuthentification.setMaximumHeight(40)
        self.setAuthentification.setMinimumWidth(200)
        self.setAuthentification.setMaximumWidth(200)
        self.setAuthentification.addItems(["Oracle Database Native"])

        self.labelUserOracle = py_label.PyLabel(
            text="Username",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.labelUserOracle.setMinimumHeight(40)
        self.labelUserOracle.setMaximumHeight(40)
        self.labelUserOracle.setMinimumWidth(200)
        self.labelUserOracle.setMaximumWidth(200)

        self.setUsernameOracle = py_line_edit.PyLineEdit(
            text="",
            place_holder_text="username",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.setUsernameOracle.setMinimumHeight(40)
        self.setUsernameOracle.setMaximumHeight(40)
        self.setUsernameOracle.setMinimumWidth(200)
        self.setUsernameOracle.setMaximumWidth(200)

        self.labelPwdOracle = py_label.PyLabel(
            text="Password",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.labelPwdOracle.setMinimumHeight(40)
        self.labelPwdOracle.setMaximumHeight(40)
        self.labelPwdOracle.setMinimumWidth(200)
        self.labelPwdOracle.setMaximumWidth(200)

        self.setPasswordOracle = py_line_edit.PyLineEdit(
            text="",
            place_holder_text="password",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"],
            echomode="PasswordEchoOnEdit"

        )
        self.setPasswordOracle.setMinimumHeight(40)
        self.setPasswordOracle.setMaximumHeight(40)
        self.setPasswordOracle.setMinimumWidth(200)

        self.isSavePwdOracle = py_radio_button.PyRadioButton(
            text="Save password",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.isSavePwdOracle.setMinimumHeight(40)
        self.isSavePwdOracle.setMaximumHeight(40)
        self.isSavePwdOracle.setMinimumWidth(200)
        self.isSavePwdOracle.setMaximumWidth(200)

        self.load_pages.authentification_layout.addWidget(
            self.labelAuthOracle, 0, 0)
        self.load_pages.authentification_layout.addWidget(
            self.setAuthentification, 0, 1)

        self.load_pages.authentification_layout.addWidget(
            self.labelUserOracle, 1, 0)
        self.load_pages.authentification_layout.addWidget(
            self.setUsernameOracle, 1, 1)
        self.load_pages.authentification_layout.addWidget(
            self.labelPwdOracle, 2, 0)
        self.load_pages.authentification_layout.addWidget(
            self.setPasswordOracle, 2, 1)
        self.load_pages.authentification_layout.addWidget(
            self.isSavePwdOracle, 2, 2)

        self.labelCustomName = py_label.PyLabel(
            text="Connexion name",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["bg_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]
        )
        self.labelCustomName.setMinimumHeight(40)
        self.labelCustomName.setMaximumHeight(40)
        self.labelCustomName.setMinimumWidth(200)
        self.labelCustomName.setMaximumWidth(200)

        self.setCustomName = py_line_edit.PyLineEdit(
            text="",
            place_holder_text="custom name",
            radius=8,
            border_size=2,
            color=self.themes["app_color"]["text_foreground"],
            selection_color=self.themes["app_color"]["white"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_active=self.themes["app_color"]["dark_three"],
            context_color=self.themes["app_color"]["context_color"]

        )
        self.setCustomName.setMinimumHeight(40)
        self.setCustomName.setMaximumHeight(40)
        self.setCustomName.setMinimumWidth(200)

        self.load_pages.settings_layout.addWidget(self.labelCustomName)
        self.load_pages.settings_layout.addWidget(self.setCustomName)

    def settings_DB_buttons(self):
        self.testDB = py_push_button.PyPushButton(
            text="Connection test",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            bg_color_disabled=self.themes["app_color"]["grey"],
            is_enabled=False
        )
        self.testDB.setMinimumHeight(40)
        self.testDB.setMaximumHeight(40)
        self.testDB.setMinimumWidth(150)
        self.testDB.setMaximumWidth(150)

        self.clearDB = py_push_button.PyPushButton(
            text="Clear",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            bg_color_disabled=self.themes["app_color"]["grey"],
            icon_path="icon_clear.svg"
        )
        self.clearDB.setMinimumHeight(40)
        self.clearDB.setMaximumHeight(40)
        self.clearDB.setMinimumWidth(150)
        self.clearDB.setMaximumWidth(150)

        self.saveDB = py_push_button.PyPushButton(
            text="Save",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            bg_color_disabled=self.themes["app_color"]["grey"],
            is_enabled=False,
            icon_path="icon_compare.svg"
        )
        self.saveDB.setMinimumHeight(40)
        self.saveDB.setMaximumHeight(40)
        self.saveDB.setMinimumWidth(150)
        self.saveDB.setMaximumWidth(150)

        self.load_pages.settings_buttons.addWidget(self.testDB)

        self.load_pages.settings_buttons.addSpacerItem(
            QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Minimum))

        self.load_pages.settings_buttons.addWidget(self.clearDB)
        self.load_pages.settings_buttons.addWidget(self.saveDB)

    def settings_left_column(self):
        pass

    def settings_right_column(self):
        self.right_btn1 = py_push_button.PyPushButton(
            text="Show Menu 2",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            bg_color_disabled=self.themes["app_color"]["grey"],
            icon_path="icon_arrow_right.svg"
        )
        self.right_btn1.setMaximumHeight(40)
        self.right_column.btn_1_layout.addWidget(self.right_btn1)

        self.right_btn2 = py_push_button.PyPushButton(
            text="Show Menu 1",
            radius=8,
            color=self.themes["app_color"]["text_foreground"],
            bg_color=self.themes["app_color"]["dark_one"],
            bg_color_hover=self.themes["app_color"]["dark_three"],
            bg_color_pressed=self.themes["app_color"]["dark_four"],
            bg_color_disabled=self.themes["app_color"]["grey"],
            icon_path="icon_arrow_left.svg"
        )
        self.right_btn2.setMaximumHeight(40)
        self.right_column.btn_2_layout.addWidget(self.right_btn2)

    def resize_grips(self):

        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.parent.height())
            self.right_grip.setGeometry(
                self.parent.width() - 15, 10, 10, self.parent.height())
            self.top_grip.setGeometry(5, 5, self.parent.width() - 10, 10)
            self.bottom_grip.setGeometry(
                5, self.parent.height() - 15, self.parent.width() - 10, 10)
            self.top_right_grip.setGeometry(
                self.parent.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(
                5, self.parent.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(
                self.parent.width() - 20, self.parent.height() - 20, 15, 15)

    def get_self(self):
        return self
