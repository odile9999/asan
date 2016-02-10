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
    plotSpecRaisedSignal = pyqtSignal(object, object, object)
    plotMassRaisedSignal = pyqtSignal(
        object, object, object, float, bool)
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
        self.ui.pushButton_UpdatePlots.setEnabled(True)

        log.info("PIPELINE started...")
        self.pip = Pipeline(filename)

        # Update parameters box
        self.parametersRaisedSignal.emit(filename, self.pip)

        # Check if data are available
        if self.pip.points > 0:
            # Update masstab_viewer box
            self.masstabRaisedSignal.emit(filename, self.pip)

            self.mass_event()
            self.peaks_event()

            self.emit_plot_signals()

    def update_pipeline(self):
        log.debug("event from %s", self.sender())
        self.pip.process_peaks(
            self.mph, self.mpd, self.peaks_x1, self.peaks_x2)
        self.ui.spinBox_PeakDistanceFound.setValue(self.pip.mpd)

    def emit_plot_signals(self):
        log.debug("event from %s", self.sender())
        # Check if data are available
        if self.pip.points > 0:
            self.update_pipeline()

            self.plotSpecRaisedSignal.emit(
                self.shortname, self.pip.spectrum, self.pip.time)

            log.debug("Emit1")

            x = np.asarray(self.pip.mass)
            log.debug("Emit2")
            print(self.mass_x1)
            print("type=", x.type())
            mask = [(x >= self.mass_x1) & (x <= self.mass_x2)]
            log.debug("Emit3")
            x = self.pip.mass[mask]
            y = self.pip.spectrum[mask]
            log.debug("Emit4")
            self.plotMassRaisedSignal.emit(
                self.shortname, y, x,
                float(self.ref_mass), bool(self.hold))
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
