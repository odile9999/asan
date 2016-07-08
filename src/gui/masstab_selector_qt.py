# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\S.O.F.T.S\PIRENEA\PYTHON\asan\src\gui\masstab_selector_qt.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget_MassTabSelector(object):
    def setupUi(self, DockWidget_MassTabSelector):
        DockWidget_MassTabSelector.setObjectName("DockWidget_MassTabSelector")
        DockWidget_MassTabSelector.resize(150, 338)
        DockWidget_MassTabSelector.setMinimumSize(QtCore.QSize(150, 300))
        DockWidget_MassTabSelector.setMaximumSize(QtCore.QSize(150, 700))
        DockWidget_MassTabSelector.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        DockWidget_MassTabSelector.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.listView_Mass = QtWidgets.QListView(self.dockWidgetContents)
        self.listView_Mass.setObjectName("listView_Mass")
        self.gridLayout.addWidget(self.listView_Mass, 0, 0, 1, 1)
        self.pushButton_ChangeList = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_ChangeList.setObjectName("pushButton_ChangeList")
        self.gridLayout.addWidget(self.pushButton_ChangeList, 1, 0, 1, 1)
        DockWidget_MassTabSelector.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget_MassTabSelector)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_MassTabSelector)

    def retranslateUi(self, DockWidget_MassTabSelector):
        _translate = QtCore.QCoreApplication.translate
        DockWidget_MassTabSelector.setWindowTitle(_translate("DockWidget_MassTabSelector", "MassTab Selector"))
        self.pushButton_ChangeList.setText(_translate("DockWidget_MassTabSelector", "Change List"))

