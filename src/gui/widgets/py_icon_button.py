# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore


class PyIconButton(QtWidgets.QPushButton):
    def __init__(
        self,
        icon_path=None,
        parent=None,
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
        dark_one="#1b1e23",
        text_foreground="#8a95aa",
        context_color="#568af2",
        top_margin=40,
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
        self._top_margin = top_margin
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
        icon = QtGui.QPixmap(image).scaled(50, 50, QtCore.Qt.KeepAspectRatio)
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
        pos_x = (pos.x() - (self._tooltip.width() // 2)) + (self.width() // 2)
        pos_y = pos.y() - self._top_margin
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
        font: 800 9pt "Segoe UI";
    }}
    """

    def __init__(
        self,
        parent,
        tooltip,
        dark_one,
        text_foreground
    ):
        QtWidgets.QLabel.__init__(self)

        style = self.style_tooltip.format(
            _dark_one=dark_one,
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
