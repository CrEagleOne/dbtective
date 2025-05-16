# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore
from gui.core import settings


class PyWindow(QtWidgets.QFrame):
    bg_style = """
    #pod_bg_app {{
        background-color: {_bg_color};
        border-radius: {_border_radius};
        border: {_border_size}px solid {_border_color};
    }}
    QFrame {{ 
        color: {_text_color};
        font: {_text_font};
    }}
    """

    def __init__(
        self,
        parent,
        layout=QtCore.Qt.Vertical,
        margin=0,
        spacing=2,
        bg_color="#2c313c",
        text_color="#fff",
        text_font="9pt 'Segoe UI'",
        border_radius=10,
        border_size=2,
        border_color="#343b48",
        enable_shadow=True
    ):
        super().__init__()

        self.settings = settings.Settings().get_settings()
        self.parent = parent
        self.layout = layout
        self.margin = margin
        self.bg_color = bg_color
        self.text_color = text_color
        self.text_font = text_font
        self.border_radius = border_radius
        self.border_size = border_size
        self.border_color = border_color
        self.enable_shadow = enable_shadow
        self.setObjectName("pod_bg_app")
        self.set_stylesheet()

        if layout == QtCore.Qt.Vertical:
            self.layout = QtWidgets.QHBoxLayout(self)
        else:
            self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(margin, margin, margin, margin)
        self.layout.setSpacing(spacing)

        if self.settings["custom_title_bar"]:
            if enable_shadow:
                self.shadow = QtWidgets.QGraphicsDropShadowEffect()
                self.shadow.setBlurRadius(20)
                self.shadow.setXOffset(0)
                self.shadow.setYOffset(0)
                self.shadow.setColor(QtGui.QColor(0, 0, 0, 160))
                self.setGraphicsEffect(self.shadow)

    def set_stylesheet(
        self,
        bg_color=None,
        border_radius=None,
        border_size=None,
        border_color=None,
        text_color=None,
        text_font=None
    ):
        if bg_color:
            internal_bg_color = bg_color
        else:
            internal_bg_color = self.bg_color

        if border_radius:
            internal_border_radius = border_radius
        else:
            internal_border_radius = self.border_radius

        if border_size:
            internal_border_size = border_size
        else:
            internal_border_size = self.border_size

        if text_color:
            internal_text_color = text_color
        else:
            internal_text_color = self.text_color

        if border_color:
            internal_border_color = border_color
        else:
            internal_border_color = self.border_color

        if text_font:
            internal_text_font = text_font
        else:
            internal_text_font = self.text_font

        self.setStyleSheet(self.bg_style.format(
            _bg_color=internal_bg_color,
            _border_radius=internal_border_radius,
            _border_size=internal_border_size,
            _border_color=internal_border_color,
            _text_color=internal_text_color,
            _text_font=internal_text_font
        ))
