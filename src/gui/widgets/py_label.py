# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore
from core.utils import common


class PyLabel(QtWidgets.QLabel):
    style = '''
        QLabel {{
            font-size: {_font_size};
            background-color: {_bg_color};
            border-radius: {_radius}px;
            border: {_border_size}px solid transparent;
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {_selection_color};
            selection-background-color: {_context_color};
            color: {_color};
        }}
        QLabel:focus {{
            border: {_border_size}px solid {_context_color};
            background-color: {_bg_color_active};

        }}
    '''

    def __init__(
        self,
        text="",
        radius=8,
        border_size=2,
        color="#FFF",
        selection_color="#FFF",
        bg_color="#333",
        bg_color_active="#222",
        context_color="#00ABE8",
        font_size="12px",
        icon_path=None,
        accept_drops=False,
    ):
        super().__init__()

        if text:
            self.setText(text)

        self.setAcceptDrops(accept_drops)

        if icon_path:
            icon = QtGui.QIcon(
                common.set_svg_icon(icon_path))
            pixmap = icon.pixmap(100, 100)

            self.setPixmap(pixmap)

        self.set_stylesheet(
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            context_color,
            font_size
        )

    def set_stylesheet(
        self,
        radius,
        border_size,
        color,
        selection_color,
        bg_color,
        bg_color_active,
        context_color,
        font_size
    ):
        style_format = self.style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _context_color=context_color,
            _font_size=font_size
        )
        self.setStyleSheet(style_format)

    def setText(self, text):
        super().setText(text)
        # Enable rich text rendering
        self.setTextFormat(QtCore.Qt.RichText)
