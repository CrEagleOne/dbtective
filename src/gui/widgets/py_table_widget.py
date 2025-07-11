# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtCore


class PyTableWidget(QtWidgets.QTableWidget):
    style = '''
        QTableWidget {{
            background-color: {_bg_color};
            padding: 5px;
            border-radius: {_radius}px;
            gridline-color: {_grid_line_color};
            color: {_color};
        }}
        QTableWidget::item{{
            border-color: none;
            padding-left: 5px;
            padding-right: 5px;
            gridline-color: rgb(44, 49, 60);
            border-bottom: 1px solid {_bottom_line_color};
        }}
        QTableWidget::item:selected{{
            background-color: {_selection_color};
        }}
        QHeaderView::section{{
            background-color: rgb(33, 37, 43);
            max-width: 30px;
            border: 1px solid rgb(44, 49, 58);
            border-style: none;
            border-bottom: 1px solid rgb(44, 49, 60);
            border-right: 1px solid rgb(44, 49, 60);
        }}
        QTableWidget::horizontalHeader {{
            background-color: rgb(33, 37, 43);
        }}
        QTableWidget QTableCornerButton::section {{
            border: none;
            background-color: {_header_horizontal_color};
            padding: 3px;
            border-top-left-radius: {_radius}px;
        }}
        QHeaderView::section:horizontal
        {{
            border: none;
            background-color: {_header_horizontal_color};
            padding: 3px;
        }}
        QHeaderView::section:vertical
        {{
            border: none;
            background-color: {_header_vertical_color};
            padding-left: 5px;
            padding-right: 5px;
            border-bottom: 1px solid {_bottom_line_color};
            margin-bottom: 1px;
        }}
        QHeaderView::down-arrow
        {{
        }}
        QHeaderView::up-arrow
        {{
        }}
        QScrollBar:horizontal {{
            border: none;
            background: {_scroll_bar_bg_color};
            height: 8px;
            margin: 0px 21px 0 21px;
            border-radius: 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: {_context_color};
            min-width: 25px;
            border-radius: 4px
        }}
        QScrollBar::add-line:horizontal {{
            border: none;
            background: {_scroll_bar_btn_color};
            width: 20px;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: right;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:horizontal {{
            border: none;
            background: {_scroll_bar_btn_color};
            width: 20px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            subcontrol-position: left;
            subcontrol-origin: margin;
        }}
        QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
        {{
            background: none;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
        {{
            background: none;
        }}
        QScrollBar:vertical {{
            border: none;
            background: {_scroll_bar_bg_color};
            width: 8px;
            margin: 21px 0 21px 0;
            border-radius: 0px;
        }}
        QScrollBar::handle:vertical {{
            background: {_context_color};
            min-height: 25px;
            border-radius: 4px
        }}
        QScrollBar::add-line:vertical {{
            border: none;
            background: {_scroll_bar_btn_color};
            height: 20px;
            border-bottom-left-radius: 4px;
            border-bottom-right-radius: 4px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }}
        QScrollBar::sub-line:vertical {{
            border: none;
            background: {_scroll_bar_btn_color};
            height: 20px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }}
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
            background: none;
        }}

        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
    '''

    def __init__(
        self,
        radius=8,
        color="#FFF",
        bg_color="#444",
        selection_color="#FFF",
        header_horizontal_color="#333",
        header_vertical_color="#444",
        bottom_line_color="#555",
        grid_line_color="#555",
        scroll_bar_bg_color="#FFF",
        scroll_bar_btn_color="#3333",
        context_color="#00ABE8",
        headers=[]
    ):
        super().__init__()

        self.setColumnCount(len(headers))

        self.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        self.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        self.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.setShowGrid(True)
        self.setGridStyle(QtCore.Qt.PenStyle.NoPen)
        self.setSortingEnabled(True)

        self.setCornerButtonEnabled(True)
        self.horizontalHeader().setCascadingSectionResizes(True)
        self.horizontalHeader().setMinimumSectionSize(100)
        self.horizontalHeader().setDefaultSectionSize(100)
        self.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().setVisible(False)

        for i, column in enumerate(headers):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setText(column)
            self.setHorizontalHeaderItem(i, item)

        self.set_stylesheet(
            radius,
            color,
            bg_color,
            header_horizontal_color,
            header_vertical_color,
            selection_color,
            bottom_line_color,
            grid_line_color,
            scroll_bar_bg_color,
            scroll_bar_btn_color,
            context_color
        )

    def set_stylesheet(
        self,
        radius,
        color,
        bg_color,
        header_horizontal_color,
        header_vertical_color,
        selection_color,
        bottom_line_color,
        grid_line_color,
        scroll_bar_bg_color,
        scroll_bar_btn_color,
        context_color
    ):
        style_format = self.style.format(
            _radius=radius,
            _color=color,
            _bg_color=bg_color,
            _header_horizontal_color=header_horizontal_color,
            _header_vertical_color=header_vertical_color,
            _selection_color=selection_color,
            _bottom_line_color=bottom_line_color,
            _grid_line_color=grid_line_color,
            _scroll_bar_bg_color=scroll_bar_bg_color,
            _scroll_bar_btn_color=scroll_bar_btn_color,
            _context_color=context_color
        )
        self.setStyleSheet(style_format)
