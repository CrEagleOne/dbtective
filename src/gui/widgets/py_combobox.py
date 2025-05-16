# -*- coding: utf-8 -*-

from PySide6 import QtWidgets


class PyComboBox(QtWidgets.QComboBox):
    style = '''
        QComboBox {{
            background-color: {_bg_color};
            border-radius: {_radius}px;
            border: {_border_size}px solid transparent;
            padding-left: 10px;
            padding-right: 10px;
            selection-color: {_selection_color};
            selection-background-color: {_context_color};
            color: {_color};
        }}
        QComboBox:focus {{
            border: {_border_size}px solid {_context_color};
            background-color: {_bg_color_active};

        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left-width: 3px;
            border-left-color: rgba(39, 44, 54, 150);
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
            background-position: center;
            background-repeat: no-reperat;
            background-image: gui/images/svg_icons/icon_arrow_down.svg;
        }}

    '''

    def __init__(
        self,
        radius=8,
        border_size=2,
        color="#FFF",
        selection_color="#FFF",
        bg_color="#333",
        bg_color_active="#222",
        context_color="#00ABE8"
    ):
        super().__init__()

        self.set_stylesheet(
            radius,
            border_size,
            color,
            selection_color,
            bg_color,
            bg_color_active,
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
        context_color
    ):
        style_format = self.style.format(
            _radius=radius,
            _border_size=border_size,
            _color=color,
            _selection_color=selection_color,
            _bg_color=bg_color,
            _bg_color_active=bg_color_active,
            _context_color=context_color
        )
        self.setStyleSheet(style_format)
