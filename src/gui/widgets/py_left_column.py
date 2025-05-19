# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore
from gui.views import ui_left_column


class PyLeftColumn(QtWidgets.QWidget):
    clicked = QtCore.Signal(object)
    released = QtCore.Signal(object)

    def __init__(
        self,
        parent,
        app_parent,
        text_title,
        text_title_size,
        text_title_color,
        dark_one,
        bg_color,
        btn_color,
        btn_color_hover,
        btn_color_pressed,
        icon_path,
        icon_color,
        icon_color_hover,
        icon_color_pressed,
        context_color,
        icon_close_path,
        radius=8
    ):
        super().__init__()

        self._parent = parent
        self._app_parent = app_parent
        self._text_title = text_title
        self._text_title_size = text_title_size
        self._text_title_color = text_title_color
        self._icon_path = icon_path
        self._dark_one = dark_one
        self._bg_color = bg_color
        self._btn_color = btn_color
        self._btn_color_hover = btn_color_hover
        self._btn_color_pressed = btn_color_pressed
        self._icon_color = icon_color
        self._icon_color_hover = icon_color_hover
        self._icon_color_pressed = icon_color_pressed
        self._context_color = context_color
        self._icon_close_path = icon_close_path
        self._radius = radius
        self.setup_ui()
        self.menus = ui_left_column.Ui_LeftColumn()
        self.menus.setupUi(self.content_frame)
        self.btn_close.clicked.connect(self.btn_clicked)
        self.btn_close.released.connect(self.btn_released)

    def btn_clicked(self):
        self.clicked.emit(self.btn_close)

    def btn_released(self):
        self.released.emit(self.btn_close)

    def setup_ui(self):
        self.base_layout = QtWidgets.QVBoxLayout(self)
        self.base_layout.setContentsMargins(0, 0, 0, 0)
        self.base_layout.setSpacing(0)
        self.title_frame = QtWidgets.QFrame()
        self.title_frame.setMaximumHeight(47)
        self.title_frame.setMinimumHeight(47)
        self.title_base_layout = QtWidgets.QVBoxLayout(self.title_frame)
        self.title_base_layout.setContentsMargins(5, 3, 5, 3)
        self.title_bg_frame = QtWidgets.QFrame()
        self.title_bg_frame.setObjectName("title_bg_frame")
        self.title_bg_frame.setStyleSheet(f'''
        #title_bg_frame {{
            background-color: {self._bg_color};
            border-radius: {self._radius}px;
        }}
        ''')
        self.title_bg_layout = QtWidgets.QHBoxLayout(self.title_bg_frame)
        self.title_bg_layout.setContentsMargins(5, 5, 5, 5)
        self.title_bg_layout.setSpacing(3)
        self.icon_frame = QtWidgets.QFrame()
        self.icon_frame.setFixedSize(30, 30)
        self.icon_frame.setStyleSheet("background: none;")
        self.icon_layout = QtWidgets.QVBoxLayout(self.icon_frame)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)
        self.icon_layout.setSpacing(5)
        self.icon = PyIcon(self._icon_path, self._icon_color)
        self.icon_layout.addWidget(
            self.icon, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
        self.title_label = QtWidgets.QLabel(self._text_title)
        self.title_label.setObjectName("title_label")
        self.title_label.setStyleSheet(f'''
        #title_label {{
            font-size: {self._text_title_size}pt;
            color: {self._text_title_color};
            padding-bottom: 2px;
            background: none;
        }}
        ''')
        self.btn_frame = QtWidgets.QFrame()
        self.btn_frame.setFixedSize(30, 30)
        self.btn_frame.setStyleSheet("background: none;")
        self.btn_close = PyLeftButton(
            self._parent,
            self._app_parent,
            tooltip_text="Hide",
            dark_one=self._dark_one,
            bg_color=self._btn_color,
            bg_color_hover=self._btn_color_hover,
            bg_color_pressed=self._btn_color_pressed,
            icon_color=self._icon_color,
            icon_color_hover=self._icon_color_hover,
            icon_color_pressed=self._icon_color_pressed,
            icon_color_active=self._icon_color_pressed,
            context_color=self._context_color,
            text_foreground=self._text_title_color,
            icon_path=self._icon_close_path,
            radius=6,
        )
        self.btn_close.setParent(self.btn_frame)
        self.btn_close.setObjectName("btn_close_left_column")
        self.title_bg_layout.addWidget(self.icon_frame)
        self.title_bg_layout.addWidget(self.title_label)
        self.title_bg_layout.addWidget(self.btn_frame)
        self.title_base_layout.addWidget(self.title_bg_frame)
        self.content_frame = QtWidgets.QFrame()
        self.content_frame.setStyleSheet("background: none")
        self.base_layout.addWidget(self.title_frame)
        self.base_layout.addWidget(self.content_frame)


class PyIcon(QtWidgets.QWidget):
    def __init__(
        self,
        icon_path,
        icon_color
    ):
        super().__init__()

        self._icon_path = icon_path
        self._icon_color = icon_color
        self.setup_ui()

    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.icon = QtWidgets.QLabel()
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.set_icon(self._icon_path, self._icon_color)
        self.layout.addWidget(self.icon)

    def set_icon(self, icon_path, icon_color=None):
        color = ""
        if icon_color:
            color = icon_color
        else:
            color = self._icon_color
        icon = QtGui.QPixmap(icon_path)
        painter = QtGui.QPainter(icon)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        painter.end()
        self.icon.setPixmap(icon)


class PyLeftButton(QtWidgets.QPushButton):
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
            brush = QtGui.QBrush(QtGui.QColor(self._bg_color_pressed))
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
            painter.fillRect(icon.rect(), self._context_color)
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
