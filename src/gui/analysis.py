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
    plotTimeRaisedSignal = pyqtSignal(object, object, object)
    plotMassRaisedSignal = pyqtSignal(object, object, object, bool)
    plotPeaksRaisedSignal = pyqtSignal(
        object, object, object, object, object, float, int, float, float)

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

    def new_analysis(self, filename):
        log.info("analysis of %s", filename)
        shortname = str(filename).split(sep="\\")
        self.shortname = shortname[-1]
        self.ui.lineEdit_File.setText(self.shortname)

        log.info("PIPELINE started...")
        self.pip = Pipeline(filename)

        # Update parameters box
        self.parametersRaisedSignal.emit(filename, self.pip)
        # Update masstab_viewer box
        self.masstabRaisedSignal.emit(filename, self.pip)
        # Update plots with user input values
        if self.pip.points > 0:
            self.ui.pushButton_UpdatePlots.setEnabled(True)
            self.mass_event()
            self.peaks_event()
            self.emit_plot_signals()

    def emit_plot_signals(self):
        log.debug("event from %s", self.sender())
        # Update plot for time
        x = self.pip.time
        y = self.pip.spectrum
        self.plotTimeRaisedSignal.emit(self.shortname, x, y)

        # Update plot for mass
        x, y = self.pip.get_x1_x2_mass(self.mass_x1, self.mass_x2)
        self.plotMassRaisedSignal.emit(self.shortname, x, y, bool(self.hold))

        # Process peaks with last input values
        mph, mpd = self.pip.process_peaks(
            self.mph, self.mpd, self.peaks_x1, self.peaks_x2)
        self.ui.spinBox_PeakDistanceFound.setValue(mpd)
        self.ui.doubleSpinBox_PeakHeightFound.setValue(mph)
        # Update plot for peaks
        print("before peaks")

        x, y, xind, yind = self.pip.get_mask_peaks()
        print("before peaks2", xind, yind)
        self.plotPeaksRaisedSignal.emit(
            self.shortname, x, y, xind, yind,
            float(self.mph), int(self.mpd), float(self.peaks_x1),
            float(self.peaks_x2))
        print("before peaks3")


#         x = self.pip.mass
#         mask = [(x >= self.mass_x1) & (x <= self.mass_x2)]
#         x = self.pip.mass[mask]
#         y = self.pip.spectrum[mask]
#         self.plotMassRaisedSignal.emit(
#             self.shortname, x, y,
#             float(self.ref_mass), float(self.cyclo_freq), float(self.mag_freq),
#             bool(self.hold))
#
#         x = self.pip.mass[mask]
#         y = self.pip.spectrum[mask]
#         log.debug("Emit4")
#         self.plotMassRaisedSignal.emit(
#             self.shortname, y, x,
#             float(self.ref_mass), bool(self.hold))
#
#         log.debug("Emit2")
#         x = self.pip.mass[self.pip.mask]
#         y = self.pip.spectrum[self.pip.mask]
#         self.plotPeaksRaisedSignal.emit(
#             self.shortname, y, x, self.pip.ind,
#             float(self.mph), int(self.mpd), float(self.peaks_x1),
#             float(self.peaks_x2))

if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
