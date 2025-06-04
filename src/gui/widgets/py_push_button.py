# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore
from core.utils import common


class PyPushButton(QtWidgets.QPushButton):
    style = '''
        QPushButton {{
            border: none;
            padding-left: 10px;
            padding-right: 5px;
            color: {_color};
            border-radius: {_radius};
            background-color: {_bg_color};
        }}
        QPushButton:hover {{
            background-color: {_bg_color_hover};
        }}
        QPushButton:pressed {{
            background-color: {_bg_color_pressed};
        }}
        QPushButton:disabled {{
            background-color: {_bg_color_disabled};
        }}
    '''

    def __init__(
        self,
        text,
        radius,
        color,
        bg_color,
        bg_color_hover,
        bg_color_pressed,
        bg_color_disabled,
        parent=None,
        is_enabled=True,
        icon_path=None,
        accept_drops=False
    ):
        super().__init__()

        self.setText(text)
        if not parent:
            self.setParent(parent)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        self.setEnabled(is_enabled)

        self.setAcceptDrops(accept_drops)

        if icon_path:
            self.setIcon(QtGui.QIcon(
                common.set_svg_icon(icon_path)))

        custom_style = self.style.format(
            _color=color,
            _radius=radius,
            _bg_color=bg_color,
            _bg_color_hover=bg_color_hover,
            _bg_color_pressed=bg_color_pressed,
            _bg_color_disabled=bg_color_disabled
        )
        self.setStyleSheet(custom_style)
