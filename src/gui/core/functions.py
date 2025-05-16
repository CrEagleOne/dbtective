from PySide6 import QtWidgets, QtCore


def set_page(self, page):
    self.load_pages.pages.setCurrentWidget(page)


def set_left_column_menu(
    self,
    menu,
    title,
    icon_path
):
    self.left_column.menus.menus.setCurrentWidget(menu)
    self.left_column.title_label.setText(title)
    self.left_column.icon.set_icon(icon_path)


def left_column_is_visible(self):
    width = self.left_column_frame.width()
    if width == 0:
        return False

    return True


def right_column_is_visible(self):
    width = self.right_column_frame.width()
    if width == 0:
        return False

    return True


def set_right_column_menu(self, menu):
    self.right_column.menus.setCurrentWidget(menu)


def get_title_bar_btn(self, object_name):
    return self.title_bar_frame.findChild(QtWidgets.QPushButton,
                                          object_name)


def get_left_menu_btn(self, object_name):
    return self.left_menu.findChild(QtWidgets.QPushButton, object_name)


def toggle_left_column(self):
    width = self.left_column_frame.width()
    right_column_width = self.right_column_frame.width()

    start_box_animation(
        self, width, right_column_width, "left")


def toggle_right_column(self):
    left_column_width = self.left_column_frame.width()
    width = self.right_column_frame.width()

    start_box_animation(
        self, left_column_width, width, "right")


def start_box_animation(self, left_box_width, right_box_width, direction):
    right_width = 0
    left_width = 0
    time_animation = self.settings["time_animation"]
    minimum_left = self.settings["left_column_size"]["minimum"]
    maximum_left = self.settings["left_column_size"]["maximum"]
    minimum_right = self.settings["right_column_size"]["minimum"]
    maximum_right = self.settings["right_column_size"]["maximum"]

    if left_box_width == minimum_left and direction == "left":
        left_width = maximum_left
    else:
        left_width = minimum_left

    if right_box_width == minimum_right and direction == "right":
        right_width = maximum_right
    else:
        right_width = minimum_right

    self.left_box = QtCore.QPropertyAnimation(
        self.left_column_frame, b"minimumWidth")
    self.left_box.setDuration(time_animation)
    self.left_box.setStartValue(left_box_width)
    self.left_box.setEndValue(left_width)
    self.left_box.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

    self.right_box = QtCore.QPropertyAnimation(
        self.right_column_frame, b"minimumWidth")
    self.right_box.setDuration(time_animation)
    self.right_box.setStartValue(right_box_width)
    self.right_box.setEndValue(right_width)
    self.right_box.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

    self.group = QtCore.QParallelAnimationGroup()
    self.group.stop()
    self.group.addAnimation(self.left_box)
    self.group.addAnimation(self.right_box)
    self.group.start()
