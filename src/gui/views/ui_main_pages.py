# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pages.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QScrollArea, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 725)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 14pt")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.welcome_base = QFrame(self.page_1)
        self.welcome_base.setObjectName(u"welcome_base")
        self.welcome_base.setMinimumSize(QSize(300, 150))
        self.welcome_base.setMaximumSize(QSize(300, 150))
        self.welcome_base.setFrameShape(QFrame.Shape.NoFrame)
        self.welcome_base.setFrameShadow(QFrame.Shadow.Raised)
        self.center_page_layout = QVBoxLayout(self.welcome_base)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName(u"center_page_layout")
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)
        self.logo = QFrame(self.welcome_base)
        self.logo.setObjectName(u"logo")
        self.logo.setMinimumSize(QSize(300, 120))
        self.logo.setMaximumSize(QSize(300, 120))
        self.logo.setFrameShape(QFrame.Shape.NoFrame)
        self.logo.setFrameShadow(QFrame.Shadow.Raised)
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.center_page_layout.addWidget(self.logo)

        self.label = QLabel(self.welcome_base)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.center_page_layout.addWidget(self.label)


        self.page_1_layout.addWidget(self.welcome_base, 0, Qt.AlignmentFlag.AlignHCenter)

        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.scroll_area = QScrollArea(self.page_2)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"background: transparent;")
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scroll_area.setWidgetResizable(True)
        self.contents = QWidget()
        self.contents.setObjectName(u"contents")
        self.contents.setGeometry(QRect(0, 0, 840, 705))
        self.contents.setStyleSheet(u"background: transparent;")
        self.verticalLayout = QVBoxLayout(self.contents)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel(self.contents)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(16)
        self.title_label.setFont(font)
        self.title_label.setStyleSheet(u"font-size: 16pt")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.title_label)

        self.description_label = QLabel(self.contents)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.description_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.description_label)

        self.row_1_layout = QHBoxLayout()
        self.row_1_layout.setObjectName(u"row_1_layout")
        self.row_1_layout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.db1 = QVBoxLayout()
        self.db1.setObjectName(u"db1")

        self.row_1_layout.addLayout(self.db1)

        self.db2 = QVBoxLayout()
        self.db2.setObjectName(u"db2")

        self.row_1_layout.addLayout(self.db2)


        self.verticalLayout.addLayout(self.row_1_layout)

        self.row_2_layout = QHBoxLayout()
        self.row_2_layout.setObjectName(u"row_2_layout")
        self.row_2_groupbox = QGroupBox(self.contents)
        self.row_2_groupbox.setObjectName(u"row_2_groupbox")
        self.row_2_groupbox.setStyleSheet(u"")
        self.horizontalLayout_8 = QHBoxLayout(self.row_2_groupbox)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_8.setContentsMargins(-1, 12, -1, -1)
        self.extraction = QGridLayout()
        self.extraction.setObjectName(u"extraction")

        self.horizontalLayout_8.addLayout(self.extraction)


        self.row_2_layout.addWidget(self.row_2_groupbox)


        self.verticalLayout.addLayout(self.row_2_layout)

        self.row_3_layout = QHBoxLayout()
        self.row_3_layout.setObjectName(u"row_3_layout")
        self.row_3_groupbox = QGroupBox(self.contents)
        self.row_3_groupbox.setObjectName(u"row_3_groupbox")
        self.row_3_groupbox.setMinimumSize(QSize(0, 50))
        self.row_3_groupbox.setStyleSheet(u"")
        self.horizontalLayout_10 = QHBoxLayout(self.row_3_groupbox)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.processing = QHBoxLayout()
        self.processing.setObjectName(u"processing")

        self.horizontalLayout_10.addLayout(self.processing)


        self.row_3_layout.addWidget(self.row_3_groupbox)


        self.verticalLayout.addLayout(self.row_3_layout)

        self.row_4_layout = QVBoxLayout()
        self.row_4_layout.setObjectName(u"row_4_layout")
        self.table_filter = QGroupBox(self.contents)
        self.table_filter.setObjectName(u"table_filter")
        self.table_filter_layout = QVBoxLayout(self.table_filter)
        self.table_filter_layout.setSpacing(0)
        self.table_filter_layout.setObjectName(u"table_filter_layout")
        self.table_filter_layout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.table_filter_layout.setContentsMargins(0, 0, 0, 2)
        self.table_buttons = QHBoxLayout()
        self.table_buttons.setObjectName(u"table_buttons")

        self.table_filter_layout.addLayout(self.table_buttons)


        self.row_4_layout.addWidget(self.table_filter)


        self.verticalLayout.addLayout(self.row_4_layout)

        self.row_5_layout = QHBoxLayout()
        self.row_5_layout.setObjectName(u"row_5_layout")

        self.verticalLayout.addLayout(self.row_5_layout)

        self.scroll_area.setWidget(self.contents)

        self.page_2_layout.addWidget(self.scroll_area)

        self.pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.scrollArea = QScrollArea(self.page_3)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setStyleSheet(u"background: transparent;")
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.contents_2 = QWidget()
        self.contents_2.setObjectName(u"contents_2")
        self.contents_2.setGeometry(QRect(0, 0, 274, 222))
        self.contents_2.setStyleSheet(u"background: transparent;")
        self.verticalLayout_3 = QVBoxLayout(self.contents_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.title_label_2 = QLabel(self.contents_2)
        self.title_label_2.setObjectName(u"title_label_2")
        self.title_label_2.setMaximumSize(QSize(16777215, 40))
        self.title_label_2.setFont(font)
        self.title_label_2.setStyleSheet(u"font-size: 16pt")
        self.title_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.title_label_2)

        self.description_label_2 = QLabel(self.contents_2)
        self.description_label_2.setObjectName(u"description_label_2")
        self.description_label_2.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.description_label_2.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.description_label_2)

        self.DB_selector = QHBoxLayout()
        self.DB_selector.setObjectName(u"DB_selector")

        self.verticalLayout_3.addLayout(self.DB_selector)

        self.Oracle = QHBoxLayout()
        self.Oracle.setObjectName(u"Oracle")
        self.oracle = QFrame(self.contents_2)
        self.oracle.setObjectName(u"oracle")
        self.oracle.setFrameShape(QFrame.Shape.StyledPanel)
        self.oracle.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.oracle)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.oracle_layout = QVBoxLayout()
        self.oracle_layout.setObjectName(u"oracle_layout")
        self.settings_oracle = QGridLayout()
        self.settings_oracle.setObjectName(u"settings_oracle")

        self.oracle_layout.addLayout(self.settings_oracle)

        self.authentification = QGroupBox(self.oracle)
        self.authentification.setObjectName(u"authentification")
        self.verticalLayout_4 = QVBoxLayout(self.authentification)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.authentification_layout = QGridLayout()
        self.authentification_layout.setObjectName(u"authentification_layout")

        self.verticalLayout_4.addLayout(self.authentification_layout)


        self.oracle_layout.addWidget(self.authentification)


        self.verticalLayout_5.addLayout(self.oracle_layout)


        self.Oracle.addWidget(self.oracle)


        self.verticalLayout_3.addLayout(self.Oracle)

        self.Settings = QHBoxLayout()
        self.Settings.setObjectName(u"Settings")
        self.settings = QFrame(self.contents_2)
        self.settings.setObjectName(u"settings")
        self.settings.setFrameShape(QFrame.Shape.StyledPanel)
        self.settings.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.settings)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.settings_layout = QHBoxLayout()
        self.settings_layout.setObjectName(u"settings_layout")

        self.verticalLayout_6.addLayout(self.settings_layout)

        self.settings_buttons = QHBoxLayout()
        self.settings_buttons.setObjectName(u"settings_buttons")

        self.verticalLayout_6.addLayout(self.settings_buttons)


        self.Settings.addWidget(self.settings)


        self.verticalLayout_3.addLayout(self.Settings)

        self.scrollArea.setWidget(self.contents_2)

        self.page_3_layout.addWidget(self.scrollArea)

        self.pages.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_2 = QVBoxLayout(self.page_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pages.addWidget(self.page_4)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.label.setText(QCoreApplication.translate("MainPages", u"Dbtective Compare Tool", None))
        self.title_label.setText(QCoreApplication.translate("MainPages", u"Compare databases", None))
        self.description_label.setText(QCoreApplication.translate("MainPages", u"Complete the following fields to start comparing the data", None))
        self.row_2_groupbox.setTitle(QCoreApplication.translate("MainPages", u"Extraction", None))
        self.row_3_groupbox.setTitle(QCoreApplication.translate("MainPages", u"Processing", None))
        self.table_filter.setTitle(QCoreApplication.translate("MainPages", u"List of tables", None))
        self.title_label_2.setText(QCoreApplication.translate("MainPages", u"add a new Database Config", None))
        self.description_label_2.setText(QCoreApplication.translate("MainPages", u"<html><head/><body><p><span style=\" font-size:9pt;\">To get started, choose the database from the following choice.<br/>Then, fill in the fields and click Save</span></p></body></html>", None))
        self.authentification.setTitle(QCoreApplication.translate("MainPages", u"Authentification", None))
    # retranslateUi

