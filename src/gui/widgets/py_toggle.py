# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore


class PyToggle(QtWidgets.QCheckBox):
    def __init__(
        self,
        width=50,
        bg_color="#777",
        circle_color="#DDD",
        active_color="#00BCFF",
        animation_curve=QtCore.QEasingCurve.OutBounce
    ):
        QtWidgets.QCheckBox.__init__(self)
        self.setFixedSize(width, 28)
        self.setCursor(QtCore.Qt.PointingHandCursor)

        # COLORS
        self._bg_color = bg_color
        self._circle_color = circle_color
        self._active_color = active_color

        self._position = 3
        self.animation = QtCore.QPropertyAnimation(self, b"position")
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(500)
        self.stateChanged.connect(self.setup_animation)

    @QtCore.Property(float)
    def position(self):
        return self._position

    @position.setter
    def position(self, pos):
        self._position = pos
        self.update()

    def setup_animation(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(4)
        self.animation.start()

    def hitButton(self, pos: QtCore.QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        p.setFont(QtGui.QFont("Segoe UI", 9))
        p.setPen(QtCore.Qt.NoPen)
        rect = QtCore.QRect(0, 0, self.width(), self.height())

        if not self.isChecked():
            p.setBrush(QtGui.QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            p.setBrush(QtGui.QColor(self._circle_color))
            p.drawEllipse(self._position, 3, 22, 22)
        else:
            p.setBrush(QtGui.QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), 28, 14, 14)
            p.setBrush(QtGui.QColor(self._circle_color))
            p.drawEllipse(self._position, 3, 22, 22)

        p.end()
