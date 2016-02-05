# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\S.O.F.T.S\PIRENEA\PYTHON\asan\src\gui\main_window_qt.ui'
#
# Created by: PyQt5 UI code generator 5.5
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setMaximumSize(QtCore.QSize(1280, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget_Plots = PlotsGUI(self.centralwidget)
        self.tabWidget_Plots.setObjectName("tabWidget_Plots")
        self.gridLayout.addWidget(self.tabWidget_Plots, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_DataSelector = DataSelectorGUI(MainWindow)
        self.dockWidget_DataSelector.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget_DataSelector.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_DataSelector.setObjectName("dockWidget_DataSelector")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockWidget_DataSelector.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_DataSelector)
        self.dockWidget_Parameters = ParametersGUI(MainWindow)
        self.dockWidget_Parameters.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget_Parameters.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_Parameters.setObjectName("dockWidget_Parameters")
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.dockWidget_Parameters.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_Parameters)
        self.dockWidget_Analysis = AnalysisGUI(MainWindow)
        self.dockWidget_Analysis.setMinimumSize(QtCore.QSize(1000, 203))
        self.dockWidget_Analysis.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget_Analysis.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidget_Analysis.setObjectName("dockWidget_Analysis")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.dockWidget_Analysis.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dockWidget_Analysis)
        self.dockWidget_MassTabSelector = MassTabSelectorGUI(MainWindow)
        self.dockWidget_MassTabSelector.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget_MassTabSelector.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_MassTabSelector.setObjectName("dockWidget_MassTabSelector")
        self.dockWidgetContents_4 = QtWidgets.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.dockWidget_MassTabSelector.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_MassTabSelector)
        self.dockWidget_MassTabViewer = MassTabViewerGUI(MainWindow)
        self.dockWidget_MassTabViewer.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidget_MassTabViewer.setObjectName("dockWidget_MassTabViewer")
        self.dockWidgetContents_5 = QtWidgets.QWidget()
        self.dockWidgetContents_5.setObjectName("dockWidgetContents_5")
        self.dockWidget_MassTabViewer.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidget_MassTabViewer)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SOFA"))

from gui.analysis import AnalysisGUI
from gui.data_selector import DataSelectorGUI
from gui.masstab_selector import MassTabSelectorGUI
from gui.masstab_viewer import MassTabViewerGUI
from gui.parameters import ParametersGUI
from gui.plots import PlotsGUI
