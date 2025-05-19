# -*- coding: utf-8 -*-

from PySide6 import QtWidgets, QtGui, QtCore


class PyGrips(QtWidgets.QWidget):
    def __init__(self, parent, position, disable_color=False):

        super().__init__()
        self.parent = parent
        self.setParent(parent)

        if position == "top_left":
            self.top_left(self)
            grip = QtWidgets.QSizeGrip(self.top_left_grip)
            grip.setFixedSize(self.top_left_grip.size())
            self.setGeometry(5, 5, 15, 15)

            if disable_color:
                self.top_left_grip.setStyleSheet("background: transparent")

        if position == "top_right":
            self.top_right(self)
            grip = QtWidgets.QSizeGrip(self.top_right_grip)
            grip.setFixedSize(self.top_right_grip.size())
            self.setGeometry(self.parent.width() - 20, 5, 15, 15)

            if disable_color:
                self.top_right_grip.setStyleSheet("background: transparent")

        if position == "bottom_left":
            self.bottom_left(self)
            grip = QtWidgets.QSizeGrip(self.bottom_left_grip)
            grip.setFixedSize(self.bottom_left_grip.size())
            self.setGeometry(5, self.parent.height() - 20, 15, 15)

            if disable_color:
                self.bottom_left_grip.setStyleSheet(
                    "background: transparent")

        if position == "bottom_right":
            self.bottom_right(self)
            grip = QtWidgets.QSizeGrip(self.bottom_right_grip)
            grip.setFixedSize(self.bottom_right_grip.size())
            self.setGeometry(self.parent.width() - 20,
                             self.parent.height() - 20, 15, 15)

            if disable_color:
                self.bottom_right_grip.setStyleSheet(
                    "background: transparent")

        if position == "top":
            self.top(self)
            self.setGeometry(0, 5, self.parent.width(), 10)
            self.setMaximumHeight(10)

            def resize_top(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(),
                             self.parent.height() - delta.y())
                geo = self.parent.geometry()
                geo.setTop(geo.bottom() - height)
                self.parent.setGeometry(geo)
                event.accept()
            self.top_grip.mouseMoveEvent = resize_top

            if disable_color:
                self.top_grip.setStyleSheet("background: transparent")

        elif position == "bottom":
            self.bottom(self)
            self.setGeometry(0, self.parent.height() -
                             10, self.parent.width(), 10)
            self.setMaximumHeight(10)

            def resize_bottom(event):
                delta = event.pos()
                height = max(self.parent.minimumHeight(),
                             self.parent.height() + delta.y())
                self.parent.resize(self.parent.width(), height)
                event.accept()
            self.bottom_grip.mouseMoveEvent = resize_bottom

            if disable_color:
                self.bottom_grip.setStyleSheet("background: transparent")

        elif position == "left":
            self.left(self)
            self.setGeometry(0, 10, 10, self.parent.height())
            self.setMaximumWidth(10)

            def resize_left(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(),
                            self.parent.width() - delta.x())
                geo = self.parent.geometry()
                geo.setLeft(geo.right() - width)
                self.parent.setGeometry(geo)
                event.accept()
            self.left_grip.mouseMoveEvent = resize_left

            if disable_color:
                self.left_grip.setStyleSheet("background: transparent")

        elif position == "right":
            self.right(self)
            self.setGeometry(self.parent.width() - 10,
                             10, 10, self.parent.height())
            self.setMaximumWidth(10)

            def resize_right(event):
                delta = event.pos()
                width = max(self.parent.minimumWidth(),
                            self.parent.width() + delta.x())
                self.parent.resize(width, self.parent.height())
                event.accept()
            self.right_grip.mouseMoveEvent = resize_right

            if disable_color:
                self.right_grip.setStyleSheet("background: transparent")

    def mouseReleaseEvent(self, event):
        self.mousePos = None

    def resizeEvent(self, event):
        if hasattr(self, 'top_grip'):
            self.top_grip.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self, 'bottom_grip'):
            self.bottom_grip.setGeometry(0, 0, self.width(), 10)

        elif hasattr(self, 'left_grip'):
            self.left_grip.setGeometry(0, 0, 10, self.height() - 20)

        elif hasattr(self, 'right_grip'):
            self.right_grip.setGeometry(0, 0, 10, self.height() - 20)

        elif hasattr(self, 'top_right_grip'):
            self.top_right_grip.setGeometry(self.width() - 15, 0, 15, 15)

        elif hasattr(self, 'bottom_left_grip'):
            self.bottom_left_grip.setGeometry(0, self.height() - 15, 15, 15)

        elif hasattr(self, 'bottom_right_grip'):
            self.bottom_right_grip.setGeometry(
                self.width() - 15, self.height() - 15, 15, 15)

    def top_left(self, form):
        self.top_left_grip = QtWidgets.QFrame(form)
        self.top_left_grip.setObjectName("top_left_grip")
        self.top_left_grip.setFixedSize(15, 15)
        self.top_left_grip.setStyleSheet(
            "background-color: #333; border: 2px solid #55FF00;")

    def top_right(self, form):
        self.top_right_grip = QtWidgets.QFrame(form)
        self.top_right_grip.setObjectName("top_right_grip")
        self.top_right_grip.setFixedSize(15, 15)
        self.top_right_grip.setStyleSheet(
            "background-color: #333; border: 2px solid #55FF00;")

    def bottom_left(self, form):
        self.bottom_left_grip = QtWidgets.QFrame(form)
        self.bottom_left_grip.setObjectName("bottom_left_grip")
        self.bottom_left_grip.setFixedSize(15, 15)
        self.bottom_left_grip.setStyleSheet(
            "background-color: #333; border: 2px solid #55FF00;")

    def bottom_right(self, form):
        self.bottom_right_grip = QtWidgets.QFrame(form)
        self.bottom_right_grip.setObjectName("bottom_right_grip")
        self.bottom_right_grip.setFixedSize(15, 15)
        self.bottom_right_grip.setStyleSheet(
            "background-color: #333; border: 2px solid #55FF00;")

    def top(self, form):
        self.top_grip = QtWidgets.QFrame(form)
        self.top_grip.setObjectName("top_grip")
        self.top_grip.setGeometry(QtCore.QRect(0, 0, 500, 10))
        self.top_grip.setStyleSheet("background-color: rgb(85, 255, 255);")
        self.top_grip.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))

    def bottom(self, form):
        self.bottom_grip = QtWidgets.QFrame(form)
        self.bottom_grip.setObjectName("bottom_grip")
        self.bottom_grip.setGeometry(QtCore.QRect(0, 0, 500, 10))
        self.bottom_grip.setStyleSheet("background-color: rgb(85, 170, 0);")
        self.bottom_grip.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))

    def left(self, form):
        self.left_grip = QtWidgets.QFrame(form)
        self.left_grip.setObjectName("left")
        self.left_grip.setGeometry(QtCore.QRect(0, 10, 10, 480))
        self.left_grip.setMinimumSize(QtCore.QSize(10, 0))
        self.left_grip.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.left_grip.setStyleSheet("background-color: rgb(255, 121, 198);")

    def right(self, form):
        self.right_grip = QtWidgets.QFrame(form)
        self.right_grip.setObjectName("right")
        self.right_grip.setGeometry(QtCore.QRect(0, 0, 10, 500))
        self.right_grip.setMinimumSize(QtCore.QSize(10, 0))
        self.right_grip.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))
        self.right_grip.setStyleSheet("background-color: rgb(255, 0, 127);")
