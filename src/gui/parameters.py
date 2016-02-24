#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
This module manages the GUI of the parameters viewer.
"""
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import pyqtSignal

from gui.parameters_qt import Ui_DockWidget_Parameters
import logging
log = logging.getLogger('root')


class ParametersGUI(QDockWidget):

    """
    classdocs
    """

    """ constructor """
    analysisRaisedSignal = pyqtSignal(str, object)

    def __init__(self, parent=None):
        super(ParametersGUI, self).__init__(parent)
        self.ui = Ui_DockWidget_Parameters()
        self.ui.setupUi(self)

    """ connect to events emitted by the data_selector """

    def setup(self, analysis):
        self.ana = analysis
        self.ana.parametersRaisedSignal.connect(self.fill_params)
        self.ui.doubleSpinBox_Tof1.valueChanged.connect(self.calib_event)
        self.ui.doubleSpinBox_Tof2.valueChanged.connect(self.calib_event)
        self.ui.doubleSpinBox_Tof3.valueChanged.connect(self.calib_event)
        self.ui.doubleSpinBox_Mass1.valueChanged.connect(self.calib_event)
        self.ui.doubleSpinBox_Mass2.valueChanged.connect(self.calib_event)
        self.ui.doubleSpinBox_Mass3.valueChanged.connect(self.calib_event)
        self.ui.pushButton_ApplyCalib.clicked.connect(self.apply_calib)

    def fill_params(self, filename, pip):
        log.debug("event from %s", self.sender())
        shortname = str(filename).split(sep="\\")
        self.ui.lineEdit_File.setText(shortname[-1])
        self.pip = pip
        self.update_header()
        if self.pip.data.isCalibAvailable:
            self.ui.groupBox_Calibration.setEnabled(False)
        else:
            self.ui.groupBox_Calibration.setEnabled(True)

    def update_header(self):
        #         self.ui.plainTextEdit_Header.clear()
        self.ui.plainTextEdit_Header.setPlainText(self.pip.data.headtext)

    def calib_event(self):
        log.debug("event from %s", self.sender())
        self.time_list = []
        self.mass_list = []
        tof1 = float(self.ui.doubleSpinBox_Tof1.value())
        tof2 = float(self.ui.doubleSpinBox_Tof2.value())
        tof3 = float(self.ui.doubleSpinBox_Tof3.value())
        mass1 = float(self.ui.doubleSpinBox_Mass1.value())
        mass2 = float(self.ui.doubleSpinBox_Mass2.value())
        mass3 = float(self.ui.doubleSpinBox_Mass3.value())
        self.time_list = [0.0, tof1, tof2, tof3]
        self.mass_list = [0.001, mass1, mass2, mass3]

    def apply_calib(self):
        log.debug("event from %s", self.sender())
        self.calib_event()
        coefs = self.pip.find_calib(self.time_list, self.mass_list)
        if len(coefs) > 0:
            self.ana.isCalibFound = True
            self.ana.coefs = coefs
        else:
            self.ana.isCalibFound = False
        self.ana.time_list = self.time_list
        self.ana.mass_list = self.mass_list
        print("self ana calib 2", self.ana.isCalibFound)

if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
