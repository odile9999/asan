# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\S.O.F.T.S\PIRENEA\PYTHON\asan\src\gui\masstab_viewer_qt.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget_MassTabViewer(object):
    def setupUi(self, DockWidget_MassTabViewer):
        DockWidget_MassTabViewer.setObjectName("DockWidget_MassTabViewer")
        DockWidget_MassTabViewer.resize(1200, 180)
        DockWidget_MassTabViewer.setMinimumSize(QtCore.QSize(800, 180))
        DockWidget_MassTabViewer.setMaximumSize(QtCore.QSize(1200, 200))
        DockWidget_MassTabViewer.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        DockWidget_MassTabViewer.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit_Viewer = QtWidgets.QPlainTextEdit(self.dockWidgetContents)
        self.plainTextEdit_Viewer.setStyleSheet("font: 8pt \"Courier\";")
        self.plainTextEdit_Viewer.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.plainTextEdit_Viewer.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.plainTextEdit_Viewer.setObjectName("plainTextEdit_Viewer")
        self.horizontalLayout.addWidget(self.plainTextEdit_Viewer)
        self.groupBox = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_Clear = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.verticalLayout.addWidget(self.pushButton_Clear)
        self.label_Accuracy = QtWidgets.QLabel(self.groupBox)
        self.label_Accuracy.setObjectName("label_Accuracy")
        self.verticalLayout.addWidget(self.label_Accuracy)
        self.doubleSpinBox_Accuracy = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_Accuracy.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.doubleSpinBox_Accuracy.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.doubleSpinBox_Accuracy.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.doubleSpinBox_Accuracy.setMaximum(1.0)
        self.doubleSpinBox_Accuracy.setSingleStep(0.1)
        self.doubleSpinBox_Accuracy.setProperty("value", 0.2)
        self.doubleSpinBox_Accuracy.setObjectName("doubleSpinBox_Accuracy")
        self.verticalLayout.addWidget(self.doubleSpinBox_Accuracy)
        self.pushButton_Automatic = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Automatic.setEnabled(False)
        self.pushButton_Automatic.setObjectName("pushButton_Automatic")
        self.verticalLayout.addWidget(self.pushButton_Automatic)
        self.pushButton_Write = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_Write.setEnabled(False)
        self.pushButton_Write.setObjectName("pushButton_Write")
        self.verticalLayout.addWidget(self.pushButton_Write)
        self.horizontalLayout.addWidget(self.groupBox)
        DockWidget_MassTabViewer.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget_MassTabViewer)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_MassTabViewer)

    def retranslateUi(self, DockWidget_MassTabViewer):
        _translate = QtCore.QCoreApplication.translate
        DockWidget_MassTabViewer.setWindowTitle(_translate("DockWidget_MassTabViewer", "MassTab Viewer"))
        self.pushButton_Clear.setText(_translate("DockWidget_MassTabViewer", "Clear"))
        self.label_Accuracy.setText(_translate("DockWidget_MassTabViewer", "Accuracy"))
        self.pushButton_Automatic.setText(_translate("DockWidget_MassTabViewer", "Automatic Fill"))
        self.pushButton_Write.setText(_translate("DockWidget_MassTabViewer", "Write to File..."))

