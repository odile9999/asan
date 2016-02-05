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
    parametersRaisedSignal = pyqtSignal(str, object)
    masstabRaisedSignal = pyqtSignal(str, object)
    plotSigRaisedSignal = pyqtSignal(object, object, object, int, int)
    plotSpecRaisedSignal = pyqtSignal(object, object, object)
    plotMassRaisedSignal = pyqtSignal(
        object, object, object, float, float, float, bool)
    plotPeaksRaisedSignal = pyqtSignal(
        object, object, object, object, float, int, float, float)

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
        self.ui.doubleSpinBox_RefMass.valueChanged.connect(self.mass_event)
        self.ui.doubleSpinBox_CycloFreq.valueChanged.connect(self.mass_event)
        self.ui.doubleSpinBox_MagFreq.valueChanged.connect(self.mass_event)
        self.ui.doubleSpinBox_PlotMassX1.valueChanged.connect(self.mass_event)
        self.ui.doubleSpinBox_PlotMassX2.valueChanged.connect(self.mass_event)
        self.ui.checkBox_Hold.stateChanged.connect(self.mass_event)
        # changes in peak GroupBox
        self.ui.doubleSpinBox_PeakHeight.valueChanged.connect(self.peaks_event)
        self.ui.spinBox_PeakDistance.valueChanged.connect(self.peaks_event)
        self.ui.doubleSpinBox_StartMass.valueChanged.connect(self.peaks_event)
        self.ui.doubleSpinBox_EndMass.valueChanged.connect(self.peaks_event)

    def mass_event(self):
        log.debug("event from %s", self.sender())
        self.ref_mass = float(self.ui.doubleSpinBox_RefMass.value())
        self.cyclo_freq = float(self.ui.doubleSpinBox_CycloFreq.value())
        self.mag_freq = float(self.ui.doubleSpinBox_MagFreq.value())
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
        # Mass calib
        self.ui.doubleSpinBox_RefMass.setValue(300.0939)
        self.ui.doubleSpinBox_CycloFreq.setValue(255.727)
        self.ui.doubleSpinBox_MagFreq.setValue(0.001)
        self.ui.doubleSpinBox_PlotMassX1.setValue(10.0)
        self.ui.doubleSpinBox_PlotMassX2.setValue(1000.0)
        self.ui.checkBox_Hold.setChecked(False)
        # peak detection
        self.ui.doubleSpinBox_PeakHeight.setValue(0.04)
        self.ui.spinBox_PeakDistance.setValue(50)
        self.ui.doubleSpinBox_StartMass.setValue(290.0)
        self.ui.doubleSpinBox_EndMass.setValue(310.0)
        # Plots
        self.ui.checkBox_AutoUpdate.setChecked(False)

    def new_analysis(self, filename):
        log.info("analysis of %s", filename)
        shortname = str(filename).split(sep="\\")
        self.shortname = shortname[-1]
        self.ui.lineEdit_File.setText(self.shortname)
        self.ui.pushButton_UpdatePlots.setEnabled(True)
        self.ui.checkBox_AutoUpdate.setEnabled(True)

        log.info("PIPELINE started...")
        self.pip = Pipeline(filename)

        # Update parameters box
        self.parametersRaisedSignal.emit(filename, self.pip)
        # Update masstab_viewer box
        self.masstabRaisedSignal.emit(filename, self.pip)

        self.ui.doubleSpinBox_Step.setValue(self.pip.step * 1e6)
        self.ui.spinBox_Points.setValue(self.pip.points)
        self.ui.spinBox_DefStartSignal.setValue(self.pip.start)
        self.ui.spinBox_DefEndSignal.setValue(self.pip.end)

        self.mass_event()
        self.peaks_event()

        if self.ui.checkBox_AutoUpdate.isChecked():
            self.emit_plot_signals()
        else:
            self.update_pipeline()

    def update_pipeline(self):
        log.debug("...")
        self.pip.process_signal(
            self.start_signal, self.end_signal, self.hann, self.half, self.zero, self.zero_twice)
        self.pip.process_spectrum(
            1000.0, self.ref_mass, self.cyclo_freq * 1e3, self.mag_freq * 1e3)
        self.pip.process_peaks(
            self.mph, self.mpd, self.peaks_x1, self.peaks_x2)
        self.ui.spinBox_PeakDistanceFound.setValue(self.pip.mpd)

    def emit_plot_signals(self):
        log.debug("event from %s", self.sender())
        self.update_pipeline()
        self.plotSigRaisedSignal.emit(
            self.shortname, self.pip.signal, float(self.step),
            int(self.start_signal), int(self.end_signal))

        self.plotSpecRaisedSignal.emit(
            self.shortname, self.pip.spectrum, self.pip.freq)

        x = self.pip.mass
        mask = [(x >= self.mass_x1) & (x <= self.mass_x2)]
        x = self.pip.mass[mask]
        y = self.pip.spectrum[mask]
        self.plotMassRaisedSignal.emit(
            self.shortname, y, x,
            float(self.ref_mass), float(self.cyclo_freq), float(self.mag_freq),
            bool(self.hold))

        x = self.pip.mass[self.pip.mask]
        y = self.pip.spectrum[self.pip.mask]
        self.plotPeaksRaisedSignal.emit(
            self.shortname, y, x, self.pip.ind,
            float(self.mph), int(self.mpd), float(self.peaks_x1),
            float(self.peaks_x2))

if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
