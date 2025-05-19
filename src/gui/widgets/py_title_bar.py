# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore, QtSvgWidgets
from core.utils import common
from gui.core import settings

_is_maximized = False
_old_size = QtCore.QSize()


class PyTitleBar(QtWidgets.QWidget):
    clicked = QtCore.Signal(object)
    released = QtCore.Signal(object)

    def __init__(
        self,
        parent,
        app_parent,
        logo_image="logo.svg",
        logo_width=40,
        buttons=None,
        dark_one="#1b1e23",
        bg_color="#343b48",
        div_color="#3c4454",
        btn_bg_color="#343b48",
        btn_bg_color_hover="#3c4454",
        btn_bg_color_pressed="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        context_color="#6c99f4",
        text_foreground="#8a95aa",
        radius=8,
        font_family="Segoe UI",
        title_size=10,
        is_custom_title_bar=True,
    ):
        super().__init__()

        self.settings = settings.Settings().get_settings()
        self._logo_image = logo_image
        self._dark_one = dark_one
        self._bg_color = bg_color
        self._div_color = div_color
        self._parent = parent
        self._app_parent = app_parent
        self._btn_bg_color = btn_bg_color
        self._btn_bg_color_hover = btn_bg_color_hover
        self._btn_bg_color_pressed = btn_bg_color_pressed
        self._context_color = context_color
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._font_family = font_family
        self._title_size = title_size
        self._text_foreground = text_foreground
        self._is_custom_title_bar = is_custom_title_bar
        self.setup_ui()
        self.bg.setStyleSheet(
            f"background-color: {bg_color}; border-radius: {radius}px;")
        self.top_logo.setMinimumWidth(logo_width)
        self.top_logo.setMaximumWidth(logo_width)

        def moveWindow(event):
            if parent.isMaximized():
                self.maximize_restore()
                curso_x = parent.pos().x()
                curso_y = event.globalPos().y() - QtGui.QCursor.pos().y()
                parent.move(curso_x, curso_y)
            if event.buttons() == QtCore.Qt.LeftButton:
                parent.move(parent.pos() + event.globalPos() - parent.dragPos)
                parent.dragPos = event.globalPos()
                event.accept()

        if is_custom_title_bar:
            self.top_logo.mouseMoveEvent = moveWindow
            self.div_1.mouseMoveEvent = moveWindow
            self.title_label.mouseMoveEvent = moveWindow
            self.div_2.mouseMoveEvent = moveWindow
            self.div_3.mouseMoveEvent = moveWindow

        if is_custom_title_bar:
            self.top_logo.mouseDoubleClickEvent = self.maximize_restore
            self.div_1.mouseDoubleClickEvent = self.maximize_restore
            self.title_label.mouseDoubleClickEvent = self.maximize_restore
            self.div_2.mouseDoubleClickEvent = self.maximize_restore

        self.bg_layout.addWidget(self.top_logo)
        self.bg_layout.addWidget(self.div_1)
        self.bg_layout.addWidget(self.title_label)
        self.bg_layout.addWidget(self.div_2)
        self.minimize_button.released.connect(parent.showMinimized)
        self.maximize_restore_button.released.connect(
            self.maximize_restore)
        self.close_button.released.connect(parent.close)
        self.bg_layout.addLayout(self.custom_buttons_layout)

        if is_custom_title_bar:
            self.bg_layout.addWidget(self.minimize_button)
            self.bg_layout.addWidget(self.maximize_restore_button)
            self.bg_layout.addWidget(self.close_button)

    def add_menus(self, parameters):
        if parameters and len(parameters) > 0:
            for parameter in parameters:
                _btn_icon = common.set_svg_icon(
                    parameter['btn_icon'])
                _btn_id = parameter['btn_id']
                _btn_tooltip = parameter['btn_tooltip']
                _is_active = parameter['is_active']

                self.menu = PyTitleButton(
                    self._parent,
                    self._app_parent,
                    btn_id=_btn_id,
                    tooltip_text=_btn_tooltip,
                    dark_one=self._dark_one,
                    bg_color=self._bg_color,
                    bg_color_hover=self._btn_bg_color_hover,
                    bg_color_pressed=self._btn_bg_color_pressed,
                    icon_color=self._icon_color,
                    icon_color_hover=self._icon_color_active,
                    icon_color_pressed=self._icon_color_pressed,
                    icon_color_active=self._icon_color_active,
                    context_color=self._context_color,
                    text_foreground=self._text_foreground,
                    icon_path=_btn_icon,
                    is_active=_is_active
                )
                self.menu.clicked.connect(self.btn_clicked)
                self.menu.released.connect(self.btn_released)

                self.custom_buttons_layout.addWidget(self.menu)

            if self._is_custom_title_bar:
                self.custom_buttons_layout.addWidget(self.div_3)

    def btn_clicked(self):
        self.clicked.emit(self.menu)

    def btn_released(self):
        self.released.emit(self.menu)

    def set_title(self, title):
        self.title_label.setText(title)

    def maximize_restore(self, e=None):
        global _is_maximized
        global _old_size

        def change_ui():
            if _is_maximized:
                self._parent.ui.central_widget_layout.setContentsMargins(
                    0, 0, 0, 0)
                self._parent.ui.window.set_stylesheet(
                    border_radius=0, border_size=0)
                self.maximize_restore_button.set_icon(
                    common.set_svg_icon("icon_restore.svg")
                )
            else:
                self._parent.ui.central_widget_layout.setContentsMargins(
                    10, 10, 10, 10)
                self._parent.ui.window.set_stylesheet(
                    border_radius=10, border_size=2)
                self.maximize_restore_button.set_icon(
                    common.set_svg_icon("icon_maximize.svg")
                )

        if self._parent.isMaximized():
            _is_maximized = False
            self._parent.showNormal()
            change_ui()
        else:
            _is_maximized = True
            _old_size = QtCore.QSize(
                self._parent.width(), self._parent.height())
            self._parent.showMaximized()
            change_ui()

    def setup_ui(self):
        self.title_bar_layout = QtWidgets.QVBoxLayout(self)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.bg = QtWidgets.QFrame()
        self.bg_layout = QtWidgets.QHBoxLayout(self.bg)
        self.bg_layout.setContentsMargins(0, 0, 5, 0)
        self.bg_layout.setSpacing(0)
        self.div_1 = PyDiv(self._div_color)
        self.div_2 = PyDiv(self._div_color)
        self.div_3 = PyDiv(self._div_color)
        self.top_logo = QtWidgets.QLabel()
        self.top_logo_layout = QtWidgets.QVBoxLayout(self.top_logo)
        self.top_logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_svg = QtSvgWidgets.QSvgWidget()
        self.logo_svg.setFixedSize(40, 40)
        self.logo_svg.load(common.set_svg_image(self._logo_image))
        self.top_logo_layout.addWidget(
            self.logo_svg)
        self.title_label = QtWidgets.QLabel()
        self.title_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.title_label.setStyleSheet(
            f'font: {self._title_size}pt "{self._font_family}"')
        self.custom_buttons_layout = QtWidgets.QHBoxLayout()
        self.custom_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_buttons_layout.setSpacing(3)

        self.minimize_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text="Close app",
            dark_one=self._dark_one,
            bg_color=self._btn_bg_color,
            bg_color_hover=self._btn_bg_color_hover,
            bg_color_pressed=self._btn_bg_color_pressed,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_active,
            context_color=self._context_color,
            text_foreground=self._text_foreground,
            radius=6,
            icon_path=common.set_svg_icon("icon_minimize.svg")
        )

        self.maximize_restore_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text="Maximize app",
            dark_one=self._dark_one,
            bg_color=self._btn_bg_color,
            bg_color_hover=self._btn_bg_color_hover,
            bg_color_pressed=self._btn_bg_color_pressed,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_active,
            context_color=self._context_color,
            text_foreground=self._text_foreground,
            radius=6,
            icon_path=common.set_svg_icon("icon_maximize.svg")
        )

        self.close_button = PyTitleButton(
            self._parent,
            self._app_parent,
            tooltip_text="Close app",
            dark_one=self._dark_one,
            bg_color=self._btn_bg_color,
            bg_color_hover=self._btn_bg_color_hover,
            bg_color_pressed=self._context_color,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_active,
            icon_color_active=self._icon_color_active,
            context_color=self._context_color,
            text_foreground=self._text_foreground,
            radius=6,
            icon_path=common.set_svg_icon("icon_close.svg")
        )

        self.title_bar_layout.addWidget(self.bg)


class PyDiv(QtWidgets.QWidget):
    def __init__(self, color):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 5, 0, 5)
        self.frame_line = QtWidgets.QFrame()
        self.frame_line.setStyleSheet(f"background: {color};")
        self.frame_line.setMaximumWidth(1)
        self.frame_line.setMinimumWidth(1)
        self.layout.addWidget(self.frame_line)
        self.setMaximumWidth(20)
        self.setMinimumWidth(20)


class PyTitleButton(QtWidgets.QPushButton):
    def __init__(
        self,
        parent,
        app_parent=None,
        tooltip_text="",
        btn_id=None,
        width=30,
        height=30,
        radius=8,
        bg_color="#343b48",
        bg_color_hover="#3c4454",
        bg_color_pressed="#2c313c",
        icon_color="#c3ccdf",
        icon_color_hover="#dce1ec",
        icon_color_pressed="#edf0f5",
        icon_color_active="#f5f6f9",
        icon_path="no_icon.svg",
        dark_one="#1b1e23",
        context_color="#568af2",
        text_foreground="#8a95aa",
        is_active=False
    ):
        super().__init__()

        self.setFixedSize(width, height)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setObjectName(btn_id)
        self._bg_color = bg_color
        self._bg_color_hover = bg_color_hover
        self._bg_color_pressed = bg_color_pressed
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._icon_color_active = icon_color_active
        self._context_color = context_color
        self._top_margin = self.height() + 6
        self._is_active = is_active
        self._set_bg_color = bg_color
        self._set_icon_path = icon_path
        self._set_icon_color = icon_color
        self._set_border_radius = radius
        self._parent = parent
        self._app_parent = app_parent
        self._tooltip_text = tooltip_text
        self._tooltip = _ToolTip(
            app_parent,
            tooltip_text,
            dark_one,
            context_color,
            text_foreground
        )
        self._tooltip.hide()

    def set_active(self, is_active):
        self._is_active = is_active
        self.repaint()

    def is_active(self):
        return self._is_active

    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        if self._is_active:
            brush = QtGui.QBrush(QtGui.QColor(self._context_color))
        else:
            brush = QtGui.QBrush(QtGui.QColor(self._set_bg_color))

        rect = QtCore.QRect(0, 0, self.width(), self.height())
        paint.setPen(QtCore.Qt.NoPen)
        paint.setBrush(brush)
        paint.drawRoundedRect(
            rect,
            self._set_border_radius,
            self._set_border_radius
        )

        self.icon_paint(paint, self._set_icon_path, rect)
        paint.end()

    def change_style(self, event):
        if event == QtCore.QEvent.Enter:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()
        elif event == QtCore.QEvent.Leave:
            self._set_bg_color = self._bg_color
            self._set_icon_color = self._icon_color
            self.repaint()
        elif event == QtCore.QEvent.MouseButtonPress:
            self._set_bg_color = self._bg_color_pressed
            self._set_icon_color = self._icon_color_pressed
            self.repaint()
        elif event == QtCore.QEvent.MouseButtonRelease:
            self._set_bg_color = self._bg_color_hover
            self._set_icon_color = self._icon_color_hover
            self.repaint()

    def enterEvent(self, event):
        self.change_style(QtCore.QEvent.Enter)
        self.move_tooltip()
        self._tooltip.show()

    def leaveEvent(self, event):
        self.change_style(QtCore.QEvent.Leave)
        self.move_tooltip()
        self._tooltip.hide()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.change_style(QtCore.QEvent.MouseButtonPress)
            self.setFocus()
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.change_style(QtCore.QEvent.MouseButtonRelease)
            return self.released.emit()

    def icon_paint(self, qp, image, rect):
        icon = QtGui.QPixmap(image)
        painter = QtGui.QPainter(icon)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        if self._is_active:
            painter.fillRect(icon.rect(), self._icon_color_active)
        else:
            painter.fillRect(icon.rect(), self._set_icon_color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )
        painter.end()

    def set_icon(self, icon_path):
        self._set_icon_path = icon_path
        self.repaint()

    def move_tooltip(self):
        gp = self.mapToGlobal(QtCore.QPoint(0, 0))
        pos = self._parent.mapFromGlobal(gp)
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self._top_margin
        self._tooltip.move(pos_x, pos_y)


class _ToolTip(QtWidgets.QLabel):
    style_tooltip = """
    QLabel {{
        background-color: {_dark_one};
        color: {_text_foreground};
        padding-left: 10px;
        padding-right: 10px;
        border-radius: 17px;
        border: 0px solid transparent;
        border-right: 3px solid {_context_color};
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
