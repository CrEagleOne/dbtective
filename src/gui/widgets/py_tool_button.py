# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore
from core.utils import common


class PyToolButton(QtWidgets.QToolButton):
    style = '''
    QToolButton {{
            background-color: {_bg_color};
            border-radius: {_radius}px;
            border: {_border_size}px solid transparent;
            color: {_color};
        }}
        QToolButton:checked {{
            background-color: {_bg_color_checked};
            color: {_color_checked};
        }}
        QToolButton:hover {{
            background-color: {_bg_color_hover};
            color: {_color_hover};
        }}

    '''

    def __init__(
        self,
        text="",
        icon_path="",
        icon_width=100,
        icon_length=100,
        place_holder_text="",
        radius=8,
        border_size=2,
        color="#FFF",
        bg_color="#333",
        bg_color_checked="1CD1D1",
        color_checked="#FFF",
        bg_color_hover="1CD1D1",
        color_hover="#FFF",
        is_checkable=False,
        is_autoexclusive=False,
        is_enabled=True,


    ):
        super().__init__()

        if text:
            self.setText(text)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)

        self.setCheckable(is_checkable)
        self.setAutoExclusive(is_autoexclusive)
        self.setAutoRaise(True)
        self.setToolButtonStyle(
            QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.setEnabled(is_enabled)

        if icon_path:
            self.setIcon(QtGui.QIcon(
                common.set_svg_icon(icon_path)))
            self.setIconSize(QtCore.QSize(icon_width, icon_length))

        self.set_stylesheet(
            radius,
            border_size,
            color,
            color_checked,
            color_hover,
            bg_color,
            bg_color_checked,
            bg_color_hover
        )

    def set_stylesheet(
        self,
        radius,
        border_size,
        color,
        color_checked,
        color_hover,
        bg_color,
        bg_color_checked,
        bg_color_hover
    ):
        style_format = self.style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _color_checked=color_checked,
            _color_hover=color_hover,
            _bg_color=bg_color,
            _bg_color_checked=bg_color_checked,
            _bg_color_hover=bg_color_hover
        )
        self.setStyleSheet(style_format)
