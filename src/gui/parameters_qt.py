# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\S.O.F.T.S\PIRENEA\PYTHON\asan\src\gui\parameters_qt.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget_Parameters(object):
    def setupUi(self, DockWidget_Parameters):
        DockWidget_Parameters.setObjectName("DockWidget_Parameters")
        DockWidget_Parameters.resize(260, 300)
        DockWidget_Parameters.setMinimumSize(QtCore.QSize(260, 200))
        DockWidget_Parameters.setMaximumSize(QtCore.QSize(280, 300))
        DockWidget_Parameters.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        DockWidget_Parameters.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.lineEdit_Date = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.lineEdit_Date.setGeometry(QtCore.QRect(60, 20, 113, 20))
        self.lineEdit_Date.setMaxLength(32763)
        self.lineEdit_Date.setObjectName("lineEdit_Date")
        self.label_Date = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_Date.setGeometry(QtCore.QRect(60, 0, 47, 13))
        self.label_Date.setObjectName("label_Date")
        self.plainTextEdit_Header = QtWidgets.QPlainTextEdit(self.dockWidgetContents)
        self.plainTextEdit_Header.setGeometry(QtCore.QRect(10, 60, 241, 201))
        self.plainTextEdit_Header.setObjectName("plainTextEdit_Header")
        self.label_Header = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_Header.setGeometry(QtCore.QRect(10, 40, 47, 13))
        self.label_Header.setObjectName("label_Header")
        DockWidget_Parameters.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget_Parameters)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_Parameters)

    def retranslateUi(self, DockWidget_Parameters):
        _translate = QtCore.QCoreApplication.translate
        DockWidget_Parameters.setWindowTitle(_translate("DockWidget_Parameters", "Parameters"))
        self.label_Date.setText(_translate("DockWidget_Parameters", "Date"))
        self.label_Header.setText(_translate("DockWidget_Parameters", "Header"))

