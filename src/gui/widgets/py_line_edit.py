# -*- coding: utf-8 -*-

from PySide6 import QtWidgets


class PyLineEdit(QtWidgets.QLineEdit):
    style = '''
        QLineEdit {{
            background-color: {_bg_color};
            border-radius: {_radius}px;
            border: {_border_size}px solid transparent;
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {_selection_color};
            selection-background-color: {_context_color};
            color: {_color};
        }}
        QLineEdit:focus {{
            border: {_border_size}px solid {_context_color};
            background-color: {_bg_color_active};
        }}
        QLineEdit:disabled {{
            background-color: {_bg_color_inactive};
        }}
    '''

    def __init__(
        self,
        text="",
        place_holder_text="",
        radius=8,
        border_size=2,
        color="#FFF",
        selection_color="#FFF",
        bg_color="#333",
        bg_color_active="#222",
        bg_color_inactive="#6f7175",
        context_color="#00ABE8",
        input_mask=None,
        echomode="normal",
        active=True
    ):
        super().__init__()

        if text:
            self.setText(text)
        if place_holder_text:
            self.setPlaceholderText(place_holder_text)
        if input_mask:
            self.setInputMask(input_mask)

        if echomode == "Password":
            self.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        elif echomode == "PasswordEchoOnEdit":
            self.setEchoMode(QtWidgets.QLineEdit.EchoMode.PasswordEchoOnEdit)
        elif echomode == "NoEcho":
            self.setEchoMode(QtWidgets.QLineEdit.EchoMode.NoEcho)

        self.setCursorPosition(0)

        if not active:
            self.setDisabled(True)

        self.set_stylesheet(
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
            bg_color_inactive,
            context_color
        )

    def set_stylesheet(
        self,
        radius,
        border_size,
        color,
        selection_color,
        bg_color,
        bg_color_active,
        bg_color_inactive,
        context_color
    ):
        style_format = self.style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _bg_color_inactive=bg_color_inactive,
            _context_color=context_color
        )
        self.setStyleSheet(style_format)
