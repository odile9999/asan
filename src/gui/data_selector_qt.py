# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\S.O.F.T.S\PIRENEA\PYTHON\asan\src\gui\data_selector_qt.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget_DataSelector(object):
    def setupUi(self, DockWidget_DataSelector):
        DockWidget_DataSelector.setObjectName("DockWidget_DataSelector")
        DockWidget_DataSelector.resize(300, 200)
        DockWidget_DataSelector.setMinimumSize(QtCore.QSize(300, 200))
        DockWidget_DataSelector.setMaximumSize(QtCore.QSize(300, 200))
        DockWidget_DataSelector.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        DockWidget_DataSelector.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.label_Folder = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_Folder.setGeometry(QtCore.QRect(9, 9, 60, 16))
        self.label_Folder.setMinimumSize(QtCore.QSize(60, 0))
        self.label_Folder.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_Folder.setObjectName("label_Folder")
        self.label_Year = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_Year.setGeometry(QtCore.QRect(9, 35, 60, 16))
        self.label_Year.setMinimumSize(QtCore.QSize(60, 0))
        self.label_Year.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_Year.setObjectName("label_Year")
        self.label_Month = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_Month.setGeometry(QtCore.QRect(9, 61, 50, 16))
        self.label_Month.setMinimumSize(QtCore.QSize(50, 0))
        self.label_Month.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_Month.setObjectName("label_Month")
        self.label_Day = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_Day.setGeometry(QtCore.QRect(9, 87, 50, 16))
        self.label_Day.setMinimumSize(QtCore.QSize(50, 0))
        self.label_Day.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_Day.setObjectName("label_Day")
        self.pushButton_StartAnalysis = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_StartAnalysis.setGeometry(QtCore.QRect(80, 150, 130, 23))
        self.pushButton_StartAnalysis.setObjectName("pushButton_StartAnalysis")
        self.lineEdit_Folder = QtWidgets.QLineEdit(self.dockWidgetContents)
        self.lineEdit_Folder.setEnabled(False)
        self.lineEdit_Folder.setGeometry(QtCore.QRect(70, 6, 221, 20))
        self.lineEdit_Folder.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_Folder.setMaximumSize(QtCore.QSize(250, 16777215))
        self.lineEdit_Folder.setReadOnly(True)
        self.lineEdit_Folder.setObjectName("lineEdit_Folder")
        self.comboBox_Day = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox_Day.setGeometry(QtCore.QRect(70, 84, 70, 20))
        self.comboBox_Day.setMinimumSize(QtCore.QSize(70, 0))
        self.comboBox_Day.setMaxVisibleItems(31)
        self.comboBox_Day.setObjectName("comboBox_Day")
        self.comboBox_Month = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox_Month.setGeometry(QtCore.QRect(70, 58, 70, 20))
        self.comboBox_Month.setMinimumSize(QtCore.QSize(70, 0))
        self.comboBox_Month.setMaxVisibleItems(12)
        self.comboBox_Month.setObjectName("comboBox_Month")
        self.comboBox_Year = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox_Year.setGeometry(QtCore.QRect(70, 32, 70, 20))
        self.comboBox_Year.setMinimumSize(QtCore.QSize(70, 0))
        self.comboBox_Year.setMaxVisibleItems(15)
        self.comboBox_Year.setObjectName("comboBox_Year")
        self.comboBox_Exp = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox_Exp.setGeometry(QtCore.QRect(70, 110, 70, 20))
        self.comboBox_Exp.setMinimumSize(QtCore.QSize(70, 0))
        self.comboBox_Exp.setMaxVisibleItems(31)
        self.comboBox_Exp.setObjectName("comboBox_Exp")
        self.label_Exp = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_Exp.setGeometry(QtCore.QRect(10, 110, 60, 16))
        self.label_Exp.setMinimumSize(QtCore.QSize(50, 0))
        self.label_Exp.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_Exp.setObjectName("label_Exp")
        self.comboBox_Number = QtWidgets.QComboBox(self.dockWidgetContents)
        self.comboBox_Number.setGeometry(QtCore.QRect(160, 110, 69, 20))
        self.comboBox_Number.setMaxVisibleItems(100)
        self.comboBox_Number.setObjectName("comboBox_Number")
        self.label_Number = QtWidgets.QLabel(self.dockWidgetContents)
        self.label_Number.setGeometry(QtCore.QRect(170, 90, 50, 16))
        self.label_Number.setObjectName("label_Number")
        self.pushButton_ChooseDirectory = QtWidgets.QPushButton(self.dockWidgetContents)
        self.pushButton_ChooseDirectory.setGeometry(QtCore.QRect(170, 32, 111, 23))
        self.pushButton_ChooseDirectory.setObjectName("pushButton_ChooseDirectory")
        DockWidget_DataSelector.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget_DataSelector)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_DataSelector)

    def retranslateUi(self, DockWidget_DataSelector):
        _translate = QtCore.QCoreApplication.translate
        DockWidget_DataSelector.setWindowTitle(_translate("DockWidget_DataSelector", "Data Selector"))
        self.label_Folder.setText(_translate("DockWidget_DataSelector", "Root"))
        self.label_Year.setText(_translate("DockWidget_DataSelector", "Year"))
        self.label_Month.setText(_translate("DockWidget_DataSelector", "Month"))
        self.label_Day.setText(_translate("DockWidget_DataSelector", "Day"))
        self.pushButton_StartAnalysis.setText(_translate("DockWidget_DataSelector", "Start Analysis"))
        self.lineEdit_Folder.setText(_translate("DockWidget_DataSelector", "C:\\Users"))
        self.label_Exp.setText(_translate("DockWidget_DataSelector", "Experiment"))
        self.label_Number.setText(_translate("DockWidget_DataSelector", "Number"))
        self.pushButton_ChooseDirectory.setText(_translate("DockWidget_DataSelector", "Change Root..."))

