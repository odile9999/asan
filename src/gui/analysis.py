#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
This module manage the GUI of the analysis.
"""
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import pyqtSignal

from gui.analysis_qt import Ui_DockWidget_Analysis
from pkg.pipeline import Pipeline
import logging
log = logging.getLogger('root')


class AnalysisGUI(QDockWidget):

    """
    classdocs
    """
    parametersRaisedSignal = pyqtSignal(object)
    masstabRaisedSignal = pyqtSignal(object)
    masstabSelectorRaisedSignal = pyqtSignal(object)
    plotTimeRaisedSignal = pyqtSignal(object, object, object)
    plotMassRaisedSignal = pyqtSignal(object, object, object, bool)
    plotCalibRaisedSignal = pyqtSignal(object, object, object, object, object)
    plotPeaksRaisedSignal = pyqtSignal(
        object, object, object, object, object, float, int, float, float)
    plotClearRaisedSignal = pyqtSignal(bool, bool, bool)

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(AnalysisGUI, self).__init__(parent)
        self.ui = Ui_DockWidget_Analysis()
        self.ui.setupUi(self)

    def setup(self, data_selector):
        self.ds = data_selector
        self.__connect_events()
        self.__fill_default_analysis()

    def __connect_events(self):
        self.ds.analysisRaisedSignal.connect(self.new_analysis)
        self.ui.pushButton_UpdatePlots.clicked.connect(self.emit_plot_signals)
        # changes in mass GroupBox
        self.ui.doubleSpinBox_PlotMassX1.valueChanged.connect(self.mass_event)
        self.ui.doubleSpinBox_PlotMassX2.valueChanged.connect(self.mass_event)
        self.ui.checkBox_Hold.stateChanged.connect(self.mass_event)
        # changes in peak GroupBox
        self.ui.doubleSpinBox_PeakHeight.valueChanged.connect(self.peaks_event)
        self.ui.spinBox_PeakDistance.valueChanged.connect(self.peaks_event)
        self.ui.doubleSpinBox_StartMass.valueChanged.connect(self.peaks_event)
        self.ui.doubleSpinBox_EndMass.valueChanged.connect(self.peaks_event)
        self.ui.pushButton_ChangeMassSelector.clicked.connect(self.emit_change_mass_selector)

    def mass_event(self):
        log.debug("event from %s", self.sender())
        self.mass_x1 = float(self.ui.doubleSpinBox_PlotMassX1.value())
        self.mass_x2 = float(self.ui.doubleSpinBox_PlotMassX2.value())
        self.hold = self.ui.checkBox_Hold.isChecked()

    def peaks_event(self):
        log.debug("event from %s", self.sender())
        self.mph = float(self.ui.doubleSpinBox_PeakHeight.value())
        self.mpd = int(self.ui.spinBox_PeakDistance.value())
        self.peaks_x1 = float(self.ui.doubleSpinBox_StartMass.value())
        self.peaks_x2 = float(self.ui.doubleSpinBox_EndMass.value())

    def __fill_default_analysis(self):
        # Plots unavailable if no data
        self.ui.pushButton_UpdatePlots.setEnabled(False)
        # Mass calib
        self.ui.doubleSpinBox_PlotMassX1.setValue(10.0)
        self.ui.doubleSpinBox_PlotMassX2.setValue(1000.0)
        self.ui.doubleSpinBox_RefMass.setValue(300.0)
        self.ui.checkBox_Hold.setChecked(False)
        # peak detection
        self.ui.doubleSpinBox_PeakHeight.setValue(400.0)
        self.ui.spinBox_PeakDistance.setValue(50)
        self.ui.doubleSpinBox_StartMass.setValue(290.0)
        self.ui.doubleSpinBox_EndMass.setValue(310.0)
        self.coefs = None
        self.mass_list = []
        self.time_list = []
        self.calib_name = ""
        self.mmass_name = ""

    def new_analysis(self, spectrum_name):
        log.info("analysis of %s", spectrum_name)
        # Ex : f:\hassan\Aroma\Spectra\XXX.txt
        self.filename = spectrum_name

        self.pip = Pipeline(spectrum_name)

        self.ui.lineEdit_File.setText(self.pip.shortname)

        # Update parameters box
        self.parametersRaisedSignal.emit(self.pip)
        # Update masstab_viewer box
        self.masstabRaisedSignal.emit(self.pip)
        # Update plots with user input values
        self.ui.pushButton_UpdatePlots.setEnabled(True)
        self.mass_event()
        self.peaks_event()
        self.emit_plot_signals()

    def emit_plot_signals(self):
        log.debug("event from %s", self.sender())
        self.emit_plot_time()

        # if calib is there, always use mass columns from file
        if self.pip.data.isCalibAvailable:
            self.plotClearRaisedSignal.emit(False, False, True)
            self.emit_plot_mass_peaks()
        else:
            if self.pip.isCalibFound:
                self.plotClearRaisedSignal.emit(False, False, False)
                self.emit_plot_mass_peaks()
                self.emit_plot_calib()
            else:
                self.plotClearRaisedSignal.emit(True, True, True)

    def emit_plot_time(self):
        # Update plot for time
        x = self.pip.data.time
        y = self.pip.data.spectrum
        self.plotTimeRaisedSignal.emit(self.pip.plot_filename, x, y)

    def emit_plot_mass_peaks(self):

        # Update plot for mass
        x = self.pip.data.mass
        y = self.pip.data.spectrum
        xmask, ymask = self.pip.get_x1_x2_mass(x, y, self.mass_x1, self.mass_x2)
        self.plotMassRaisedSignal.emit(
            self.pip.plot_filename, xmask, ymask, bool(self.hold))
        # Process peaks with last input values
        mph, mpd, x, y, xind, yind = self.pip.process_peaks(x, y, self.mph, self.mpd,
                                                            self.peaks_x1, self.peaks_x2)
        self.ui.spinBox_PeakDistanceFound.setValue(mpd)
        self.ui.doubleSpinBox_PeakHeightFound.setValue(mph)
        # Update plot for peaks
        self.plotPeaksRaisedSignal.emit(
            self.pip.plot_filename, x, y, xind, yind,
            float(self.mph), int(self.mpd), float(self.peaks_x1),
            float(self.peaks_x2))

    def emit_change_mass_selector(self):
        # Update plot for mass
        x = self.pip.data.mass
        y = self.pip.data.spectrum
        mph, mpd, x, y, xind, yind = self.pip.process_peaks(x, y, self.mph, self.mpd,
                                                            self.peaks_x1, self.peaks_x2)
        # Update plot for peaks
        self.masstabSelectorRaisedSignal.emit(xind)

    def emit_plot_calib(self):
        #         log.debug("event from %s", self.sender())
        x = self.pip.data.mass
        y = self.pip.data.time
        self.plotCalibRaisedSignal.emit(
            self.pip.plot_filename, self.mass_list, self.time_list, x, y)

if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
