from automation.loopremovedialogbox import LoopRemoveDialog

from PyQt5 import QtCore, QtWidgets


class Ui_Loop(object):
    index = 0
########## Setup Loop Start/End/Sleep ############

    def setupUi(self, parent, action):
        self.objectName = "loopEnd"
        self.layoutWidget = QtWidgets.QWidget(parent.scrollAreaWidgetContents)
        self.layoutWidget.setGeometry(QtCore.QRect(
            0, parent.axis_y, int(parent.scrollArea.size().width()-20), 29))
        parent.axis_y += 30
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.layoutWidget.setLayout(self.horizontalLayout)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_LoopStartEnd = QtWidgets.QLabel(self.layoutWidget)
        self.label_LoopStartEnd.setObjectName("LoopStartEnd")
        self.horizontalLayout.addWidget(self.label_LoopStartEnd)
        if action == 'start':
            self.objectName = "loopStart"
            self.label_count = QtWidgets.QLabel(self.layoutWidget)
            self.label_count.setObjectName("label")
            self.label_count.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout.addWidget(self.label_count)
            self.spinbox_count = QtWidgets.QSpinBox(self.layoutWidget)
            self.spinbox_count.setObjectName("spinbox_count")
            self.spinbox_count.setMaximum(1000)
            self.spinbox_count.setMinimum(1)
            self.spinbox_count.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout.addWidget(self.spinbox_count)
            self.label_interval = QtWidgets.QLabel(self.layoutWidget)
            self.label_interval.setObjectName("label_interval")
            self.label_interval.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout.addWidget(self.label_interval)
            self.spinbox_interval = QtWidgets.QSpinBox(self.layoutWidget)
            self.spinbox_interval.setObjectName("spinbox_interval")
            self.spinbox_interval.setAlignment(QtCore.Qt.AlignCenter)
            self.spinbox_interval.setMaximum(1000)
            self.spinbox_interval.setMinimum(1)
            self.horizontalLayout.addWidget(self.spinbox_interval)
        elif action == 'sleep':
            self.objectName = "sleep"
            self.label_interval = QtWidgets.QLabel(self.layoutWidget)
            self.label_interval.setObjectName("label_interval")
            self.label_interval.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout.addWidget(self.label_interval)
            self.spinbox_interval = QtWidgets.QSpinBox(self.layoutWidget)
            self.spinbox_interval.setObjectName("spinbox_interval")
            self.spinbox_interval.setMaximum(1000)
            self.spinbox_interval.setMinimum(1)
            self.spinbox_interval.setAlignment(QtCore.Qt.AlignCenter)
            self.horizontalLayout.addWidget(self.spinbox_interval)
            self.btn_up = QtWidgets.QToolButton(self.layoutWidget)
            self.btn_up.setObjectName("UP")
            self.btn_up.clicked.connect(
                lambda: self.move_up_down("UP", parent))
            self.btn_down = QtWidgets.QToolButton(self.layoutWidget)
            self.btn_down.setObjectName("Down")
            self.btn_down.clicked.connect(
                lambda: self.move_up_down("DOWN", parent))

        self.btn_insert = QtWidgets.QToolButton(self.layoutWidget)
        self.btn_insert.setObjectName("insert")
        self.btn_insert.clicked.connect(lambda: self.addnew(parent))
        self.horizontalLayout.addWidget(self.btn_insert)
        self.btn_remove = QtWidgets.QToolButton(self.layoutWidget)
        self.btn_remove.setObjectName("remove")
        self.horizontalLayout.addWidget(self.btn_remove)

        self.retranslateUi(parent, action)
        QtCore.QMetaObject.connectSlotsByName(parent)

    def retranslateUi(self, parent, action):
        _translate = QtCore.QCoreApplication.translate
        if action == 'start':
            self.label_LoopStartEnd.setText(_translate("parent", "LoopStart"))
            self.label_count.setText(_translate("parent", "Count:"))
            self.label_interval.setText(_translate("parent", "Interval"))
            self.btn_remove.clicked.connect(
                lambda: self.deleteloop(parent, 'end'))
            self.label_LoopStartEnd.setStyleSheet(
                "background-color: lightgreen; border: 1px solid black")

        elif action == 'sleep':
            self.label_LoopStartEnd.setText(_translate("parent", "Sleep"))
            self.label_LoopStartEnd.setStyleSheet(
                "background-color: rgb(119, 118, 123); border: 1px solid black")
            self.label_interval.setText(_translate("parent", "Interval:"))
            self.btn_remove.clicked.connect(lambda: self.deleteSelf(parent))
            self.horizontalLayout.addWidget(self.btn_up)
            self.horizontalLayout.addWidget(self.btn_down)

            self.btn_up.setText(_translate("parent", "↑"))
            self.btn_down.setText(_translate("parent", "↓"))

        else:
            self.label_LoopStartEnd.setText(_translate("parent", "LoopEnd"))
            self.btn_remove.clicked.connect(
                lambda: self.deleteloop(parent, 'start'))
            self.label_LoopStartEnd.setStyleSheet(
                "background-color: lightgreen; border: 1px solid black")

        self.btn_insert.setText(_translate("parent", "+"))
        self.label_LoopStartEnd.setAlignment(QtCore.Qt.AlignCenter)
        self.btn_remove.setText(_translate("parent", "-"))

    def deleteSelf(self, parent):
        self.layoutWidget.setParent(None)
        self.layoutWidget.deleteLater
        parent.axis_y -= 30
        parent.objs.remove(self)
        parent.adjustGeometry()

    def addnew(self, parent):
        parent.insertDialog(self.index)

    def deleteloop(self, parent, find_obj):
        x = parent.findLoopStartEnd(find_obj, self.index)
        if x == -1:
            x = self.index
            parent.clear(x, x)
            parent.btn_LoopStartEnd.setChecked(False)
            parent.btn_LoopStartEnd.setText('Loop Start/End')
            return
        else:

            if find_obj == 'start':
                start = x
                stop = self.index
            else:
                start = self.index
                stop = x

            self.diag = LoopRemoveDialog()
            self.diag.buttonBox.accepted.connect(
                lambda: parent.clear(start, stop))

    def move_up_down(self, move, parent):
        y_axis = self.layoutWidget.pos().y()
        if move == "UP":
            if self.index > 0:
                parent.swap(self.index-1, y_axis-30)
        elif move == "DOWN":
            if self.index+1 < len(parent.objs):
                parent.swap(self.index, y_axis)
