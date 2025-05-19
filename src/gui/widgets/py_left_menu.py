# -*- coding: utf-8 -*-

import os
from PySide6 import QtWidgets, QtGui, QtCore
from core.utils import common


class PyLeftMenu(QtWidgets.QWidget):
    clicked = QtCore.Signal(object)
    released = QtCore.Signal(object)

    def __init__(
        self,
        parent=None,
        app_parent=None,
        dark_one="#1b1e23",
        dark_three="#21252d",
        dark_four="#272c36",
        bg_one="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        context_color="#568af2",
        text_foreground="#8a95aa",
        text_active="#dce1ec",
        duration_time=500,
        radius=8,
        minimum_width=50,
        maximum_width=240,
        icon_path="icon_menu.svg",
        icon_path_close="icon_menu_close.svg",
        toggle_text="Hide Menu",
        toggle_tooltip="Show menu"
    ):
        super().__init__()

        self._dark_one = dark_one
        self._dark_three = dark_three
        self._dark_four = dark_four
        self._bg_one = bg_one
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._context_color = context_color
        self._text_foreground = text_foreground
        self._text_active = text_active
        self._duration_time = duration_time
        self._radius = radius
        self._minimum_width = minimum_width
        self._maximum_width = maximum_width
        self._icon_path = common.set_svg_icon(icon_path)
        self._icon_path_close = common.set_svg_icon(
            icon_path_close)
        self._parent = parent
        self._app_parent = app_parent
        self.setup_ui()
        self.bg.setStyleSheet(
            f"background: {dark_one}; border-radius: {radius};")

        self.toggle_button = PyLeftMenuButton(
            app_parent,
            text=toggle_text,
            tooltip_text=toggle_tooltip,
            dark_one=self._dark_one,
            dark_three=self._dark_three,
            dark_four=self._dark_four,
            bg_one=self._bg_one,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_active,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_active,
            context_color=self._context_color,
            text_foreground=self._text_foreground,
            text_active=self._text_active,
            icon_path=icon_path
        )
        self.toggle_button.clicked.connect(self.toggle_animation)
        self.div_top = PyDiv(dark_four)
        self.top_layout.addWidget(self.toggle_button)
        self.top_layout.addWidget(self.div_top)
        self.div_bottom = PyDiv(dark_four)
        self.div_bottom.hide()
        self.bottom_layout.addWidget(self.div_bottom)

    def add_menus(self, parameters):
        if parameters:
            for parameter in parameters:
                _btn_icon = parameter['btn_icon']
                _btn_id = parameter['btn_id']
                _btn_text = parameter['btn_text']
                _btn_tooltip = parameter['btn_tooltip']
                _show_top = parameter['show_top']
                _is_active = parameter['is_active']

                self.menu = PyLeftMenuButton(
                    self._app_parent,
                    text=_btn_text,
                    btn_id=_btn_id,
                    tooltip_text=_btn_tooltip,
                    dark_one=self._dark_one,
                    dark_three=self._dark_three,
                    dark_four=self._dark_four,
                    bg_one=self._bg_one,
                    icon_color=self._icon_color,
                    icon_color_hover=self._icon_color_active,
                    icon_color_pressed=self._icon_color_pressed,
                    icon_color_active=self._icon_color_active,
                    context_color=self._context_color,
                    text_foreground=self._text_foreground,
                    text_active=self._text_active,
                    icon_path=_btn_icon,
                    is_active=_is_active
                )
                self.menu.clicked.connect(self.btn_clicked)
                self.menu.released.connect(self.btn_released)

                if _show_top:
                    self.top_layout.addWidget(self.menu)
                else:
                    self.div_bottom.show()
                    self.bottom_layout.addWidget(self.menu)

    def btn_clicked(self):
        self.clicked.emit(self.menu)

    def btn_released(self):
        self.released.emit(self.menu)

    def toggle_animation(self):
        self.animation = QtCore.QPropertyAnimation(
            self._parent, b"minimumWidth")
        self.animation.stop()
        if self.width() == self._minimum_width:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self._maximum_width)
            self.toggle_button.set_active_toggle(True)
            self.toggle_button.set_icon(self._icon_path_close)
        else:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(self._minimum_width)
            self.toggle_button.set_active_toggle(False)
            self.toggle_button.set_icon(self._icon_path)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutCubic)
        self.animation.setDuration(self._duration_time)
        self.animation.start()

    def select_only_one(self, widget: str):
        for btn in self.findChildren(QtWidgets.QPushButton):
            if btn.objectName() == widget:
                btn.set_active(True)
            else:
                btn.set_active(False)

    def select_only_one_tab(self, widget: str):
        for btn in self.findChildren(QtWidgets.QPushButton):
            if btn.objectName() == widget:
                btn.set_active_tab(True)
            else:
                btn.set_active_tab(False)

    def deselect_all(self):
        for btn in self.findChildren(QtWidgets.QPushButton):
            btn.set_active(False)

    def deselect_all_tab(self):
        for btn in self.findChildren(QtWidgets.QPushButton):
            btn.set_active_tab(False)

    def setup_ui(self):
        self.left_menu_layout = QtWidgets.QVBoxLayout(self)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.bg = QtWidgets.QFrame()
        self.top_frame = QtWidgets.QFrame()
        self.bottom_frame = QtWidgets.QFrame()
        self._layout = QtWidgets.QVBoxLayout(self.bg)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout = QtWidgets.QVBoxLayout(self.top_frame)
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.top_layout.setSpacing(1)
        self.bottom_layout = QtWidgets.QVBoxLayout(self.bottom_frame)
        self.bottom_layout.setContentsMargins(0, 0, 0, 8)
        self.bottom_layout.setSpacing(1)
        self._layout.addWidget(self.top_frame, 0, QtCore.Qt.AlignTop)
        self._layout.addWidget(self.bottom_frame, 0, QtCore.Qt.AlignBottom)
        self.left_menu_layout.addWidget(self.bg)


class PyDiv(QtWidgets.QWidget):
    def __init__(self, color):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.frame_line = QtWidgets.QFrame()
        self.frame_line.setStyleSheet(f"background: {color};")
        self.frame_line.setMaximumHeight(1)
        self.frame_line.setMinimumHeight(1)
        self.layout.addWidget(self.frame_line)
        self.setMaximumHeight(1)


class PyLeftMenuButton(QtWidgets.QPushButton):
    def __init__(
        self,
        app_parent,
        text,
        btn_id=None,
        tooltip_text="",
        margin=4,
        dark_one="#1b1e23",
        dark_three="#21252d",
        dark_four="#272c36",
        bg_one="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        context_color="#568af2",
        text_foreground="#8a95aa",
        text_active="#dce1ec",
        icon_path="icon_add_user.svg",
        icon_active_menu="active_menu.svg",
        is_active=False,
        is_active_tab=False,
        is_toggle_active=False
    ):
        super().__init__()
        self.setText(text)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)
        self.setObjectName(btn_id)
        self._icon_path = common.set_svg_icon(icon_path)
        self._icon_active_menu = common.set_svg_icon(
            icon_active_menu)
        self._margin = margin
        self._dark_one = dark_one
        self._dark_three = dark_three
        self._dark_four = dark_four
        self._bg_one = bg_one
        self._context_color = context_color
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._set_icon_color = self._icon_color
        self._set_bg_color = self._dark_one
        self._set_text_foreground = text_foreground
        self._set_text_active = text_active
        self._parent = app_parent
        self._is_active = is_active
        self._is_active_tab = is_active_tab
        self._is_toggle_active = is_toggle_active
        self._tooltip_text = tooltip_text
        self.tooltip = _ToolTip(
            app_parent,
            tooltip_text,
            dark_one,
            context_color,
            text_foreground
        )
        self.tooltip.hide()

    def paintEvent(self, event):
        p = QtGui.QPainter()
        p.begin(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setPen(QtCore.Qt.NoPen)
        p.setFont(self.font())
        rect_inside = QtCore.QRect(4, 5, self.width() - 8, self.height() - 10)
        rect_icon = QtCore.QRect(0, 0, 50, self.height())
        rect_blue = QtCore.QRect(4, 5, 20, self.height() - 10)
        rect_inside_active = QtCore.QRect(
            7, 5, self.width(), self.height() - 10)
        rect_text = QtCore.QRect(45, 0, self.width() - 50, self.height())

        if self._is_active:
            p.setBrush(QtGui.QColor(self._context_color))
            p.drawRoundedRect(rect_blue, 8, 8)
            p.setBrush(QtGui.QColor(self._bg_one))
            p.drawRoundedRect(rect_inside_active, 8, 8)
            icon_path = self._icon_active_menu
            app_path = os.path.abspath(os.getcwd())
            icon_path = os.path.normpath(os.path.join(app_path, icon_path))
            self._set_icon_color = self._icon_color_active
            self.icon_active(p, icon_path, self.width())
            p.setPen(QtGui.QColor(self._set_text_active))
            p.drawText(rect_text, QtCore.Qt.AlignVCenter, self.text())
            self.icon_paint(p, self._icon_path, rect_icon,
                            self._set_icon_color)

        elif self._is_active_tab:
            p.setBrush(QtGui.QColor(self._dark_four))
            p.drawRoundedRect(rect_blue, 8, 8)
            p.setBrush(QtGui.QColor(self._bg_one))
            p.drawRoundedRect(rect_inside_active, 8, 8)
            icon_path = self._icon_active_menu
            app_path = os.path.abspath(os.getcwd())
            icon_path = os.path.normpath(os.path.join(app_path, icon_path))
            self._set_icon_color = self._icon_color_active
            self.icon_active(p, icon_path, self.width())
            p.setPen(QtGui.QColor(self._set_text_active))
            p.drawText(rect_text, QtCore.Qt.AlignVCenter, self.text())
            self.icon_paint(p, self._icon_path, rect_icon,
                            self._set_icon_color)

        else:
            if self._is_toggle_active:
                p.setBrush(QtGui.QColor(self._dark_three))
                p.drawRoundedRect(rect_inside, 8, 8)
                p.setPen(QtGui.QColor(self._set_text_foreground))
                p.drawText(rect_text, QtCore.Qt.AlignVCenter, self.text())
                if self._is_toggle_active:
                    self.icon_paint(p, self._icon_path,
                                    rect_icon, self._context_color)
                else:
                    self.icon_paint(p, self._icon_path,
                                    rect_icon, self._set_icon_color)
            else:
                p.setBrush(QtGui.QColor(self._set_bg_color))
                p.drawRoundedRect(rect_inside, 8, 8)
                p.setPen(QtGui.QColor(self._set_text_foreground))
                p.drawText(rect_text, QtCore.Qt.AlignVCenter, self.text())
                self.icon_paint(p, self._icon_path, rect_icon,
                                self._set_icon_color)

        p.end()

    def set_active(self, is_active):
        self._is_active = is_active
        if not is_active:
            self._set_icon_color = self._icon_color
            self._set_bg_color = self._dark_one

        self.repaint()

    def set_active_tab(self, is_active):
        self._is_active_tab = is_active
        if not is_active:
            self._set_icon_color = self._icon_color
            self._set_bg_color = self._dark_one

        self.repaint()

    def is_active(self):
        return self._is_active

    def is_active_tab(self):
        return self._is_active_tab

    def set_active_toggle(self, is_active):
        self._is_toggle_active = is_active

    def set_icon(self, icon_path):
        self._icon_path = icon_path
        self.repaint()

    def icon_paint(self, qp, image, rect, color):
        icon = QtGui.QPixmap(image)
        painter = QtGui.QPainter(icon)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )
        painter.end()

    def icon_active(self, qp, image, width):
        icon = QtGui.QPixmap(image)
        painter = QtGui.QPainter(icon)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), self._bg_one)
        qp.drawPixmap(width - 5, 0, icon)
        painter.end()

    def change_style(self, event):
        if event == QtCore.QEvent.Enter:
            if not self._is_active:
                self._set_icon_color = self._icon_color_hover
                self._set_bg_color = self._dark_three
            self.repaint()
        elif event == QtCore.QEvent.Leave:
            if not self._is_active:
                self._set_icon_color = self._icon_color
                self._set_bg_color = self._dark_one
            self.repaint()
        elif event == QtCore.QEvent.MouseButtonPress:
            if not self._is_active:
                self._set_icon_color = self._context_color
                self._set_bg_color = self._dark_four
            self.repaint()
        elif event == QtCore.QEvent.MouseButtonRelease:
            if not self._is_active:
                self._set_icon_color = self._icon_color_hover
                self._set_bg_color = self._dark_three
            self.repaint()

    def enterEvent(self, event):
        self.change_style(QtCore.QEvent.Enter)
        if self.width() == 50 and self._tooltip_text:
            self.move_tooltip()
            self.tooltip.show()

    def leaveEvent(self, event):
        self.change_style(QtCore.QEvent.Leave)
        self.tooltip.hide()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.change_style(QtCore.QEvent.MouseButtonPress)
            self.tooltip.hide()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.change_style(QtCore.QEvent.MouseButtonRelease)
            return self.released.emit()

    def move_tooltip(self):
        gp = self.mapToGlobal(QtCore.QPoint(0, 0))
        pos = self._parent.mapFromGlobal(gp)
        pos_x = pos.x() + self.width() + 5
        pos_y = pos.y() + (self.width() - self.tooltip.height()) // 2
        self.tooltip.move(pos_x, pos_y)


class _ToolTip(QtWidgets.QLabel):
    style_tooltip = """
    QLabel {{
        background-color: {_dark_one};
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        border-left: 3px solid {_context_color};
        font: 800 9pt "Segoe UI";
    }}
    """

    def __init__(
        self,
        parent,
        tooltip,
        dark_one,
        context_color,
        text_foreground
    ):
        QtWidgets.QLabel.__init__(self)

        style = self.style_tooltip.format(
            _dark_one=dark_one,
            _context_color=context_color,
            _text_foreground=text_foreground
        )
        self.setObjectName(u"label_tooltip")
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setParent(parent)
        self.setText(tooltip)
        self.adjustSize()
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
