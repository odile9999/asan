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
        self.ui.pushButton_ChangeCalib.clicked.connect(self.change_calib)
        self.ui.pushButton_ApplyCalib.clicked.connect(self.apply_calib)
        self.ui.pushButton_SaveCalibData.clicked.connect(self.write_calib_data)
        self.ui.pushButton_SaveMmassData.clicked.connect(self.write_mmass_data)

    def fill_params(self, pip):
        log.debug("event from %s", self.sender())
        self.pip = pip
        self.ui.lineEdit_File.setText(self.pip.shortname)
        self.update_header()
        if self.pip.data.isCalibAvailable:
            self.ui.groupBox_Calibration.setEnabled(False)
            self.ui.pushButton_ChangeCalib.setEnabled(True)
            self.ui.pushButton_ApplyCalib.setEnabled(False)
            self.ui.pushButton_SaveCalibData.setEnabled(False)
        else:
            self.ui.groupBox_Calibration.setEnabled(True)
            self.ui.pushButton_ChangeCalib.setEnabled(False)
            self.ui.pushButton_ApplyCalib.setEnabled(True)
            self.ui.pushButton_SaveCalibData.setEnabled(False)

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
        self.pip.calib(self.time_list, self.mass_list)
        self.ana.time_list = self.time_list
        self.ana.mass_list = self.mass_list
        if self.pip.isCalibFound:
            self.ui.pushButton_SaveCalibData.setEnabled(True)
            self.ui.pushButton_SaveMmassData.setEnabled(True)

    def change_calib(self):
        log.debug("event from %s", self.sender())
        self.ui.groupBox_Calibration.setEnabled(True)
        self.ui.pushButton_ChangeCalib.setEnabled(False)
        self.ui.pushButton_ApplyCalib.setEnabled(True)
        self.ui.pushButton_SaveCalibData.setEnabled(False)
        self.pip.data.isCalibAvailable = False

    def write_calib_data(self):
        log.debug("event from %s", self.sender())
        self.pip.write_calib_data()

    def write_mmass_data(self):
        log.debug("event from %s", self.sender())
        self.pip.write_mmass_data()

if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
