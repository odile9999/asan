# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\S.O.F.T.S\PIRENEA\PYTHON\asan\src\gui\plots_qt.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TabWidget_Plots(object):
    def setupUi(self, TabWidget_Plots):
        TabWidget_Plots.setObjectName("TabWidget_Plots")
        TabWidget_Plots.resize(800, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TabWidget_Plots.sizePolicy().hasHeightForWidth())
        TabWidget_Plots.setSizePolicy(sizePolicy)
        TabWidget_Plots.setMinimumSize(QtCore.QSize(800, 500))
        TabWidget_Plots.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_Time = QtWidgets.QWidget()
        self.tab_Time.setObjectName("tab_Time")
        self.verticalLayout_1 = QtWidgets.QVBoxLayout(self.tab_Time)
        self.verticalLayout_1.setObjectName("verticalLayout_1")
        TabWidget_Plots.addTab(self.tab_Time, "")
        self.tab_Mass = QtWidgets.QWidget()
        self.tab_Mass.setObjectName("tab_Mass")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_Mass)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        TabWidget_Plots.addTab(self.tab_Mass, "")
        self.tab_Peaks = QtWidgets.QWidget()
        self.tab_Peaks.setObjectName("tab_Peaks")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_Peaks)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        TabWidget_Plots.addTab(self.tab_Peaks, "")
        self.tab_Calib = QtWidgets.QWidget()
        self.tab_Calib.setObjectName("tab_Calib")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_Calib)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        TabWidget_Plots.addTab(self.tab_Calib, "")

        self.retranslateUi(TabWidget_Plots)
        TabWidget_Plots.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(TabWidget_Plots)

    def retranslateUi(self, TabWidget_Plots):
        _translate = QtCore.QCoreApplication.translate
        TabWidget_Plots.setWindowTitle(_translate("TabWidget_Plots", "TabWidget"))
        TabWidget_Plots.setTabText(TabWidget_Plots.indexOf(self.tab_Time), _translate("TabWidget_Plots", "Time"))
        TabWidget_Plots.setTabText(TabWidget_Plots.indexOf(self.tab_Mass), _translate("TabWidget_Plots", "Mass"))
        TabWidget_Plots.setTabText(TabWidget_Plots.indexOf(self.tab_Peaks), _translate("TabWidget_Plots", "Peaks"))
        TabWidget_Plots.setTabText(TabWidget_Plots.indexOf(self.tab_Calib), _translate("TabWidget_Plots", "Calib"))

