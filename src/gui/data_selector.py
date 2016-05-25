#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
This module manages the GUI of the data selector.
"""
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import pyqtSignal

from gui.data_selector_qt import Ui_DockWidget_DataSelector
from pkg.filenames import FilesAndDirs

import logging
log = logging.getLogger('root')


class DataSelectorGUI(QDockWidget):

    analysisRaisedSignal = pyqtSignal(str)
    masstabRaisedSignal = pyqtSignal(str)

    """ constructor """

    def __init__(self, parent=None):
        super(DataSelectorGUI, self).__init__(parent)
        self.ui = Ui_DockWidget_DataSelector()
        self.ui.setupUi(self)
        self.filesAndDirs = FilesAndDirs()

    def setup(self):
        self.connect_events()
        self.fill_year()

    def connect_events(self):
        self.ui.lineEdit_Folder.textChanged.connect(self.fill_year)
        self.ui.comboBox_Year.currentIndexChanged.connect(self.fill_month)
        self.ui.comboBox_Month.currentIndexChanged.connect(self.fill_day)
        self.ui.comboBox_Day.currentIndexChanged.connect(self.fill_exp)
        self.ui.comboBox_Exp.currentIndexChanged.connect(self.fill_spectra)
#         self.ui.checkBox_AutoUpdate.stateChanged.connect(self.toggle_update)
        self.ui.pushButton_StartAnalysis.clicked.connect(self.emit_signals)

    def fill_year(self):
        log.debug("event from %s", self.sender())
        self.ui.comboBox_Year.clear()
        self.folder = self.ui.lineEdit_Folder.text()
        li = self.filesAndDirs.get_years(self.folder)
        if li:
            self.ui.comboBox_Year.addItems(li)

    def fill_month(self):
        log.debug("event from %s", self.sender())
        self.ui.comboBox_Month.clear()
        self.year = self.ui.comboBox_Year.currentText()
        if self.year:
            months = self.filesAndDirs.get_months(int(self.year))
            if months:
                self.ui.comboBox_Month.addItems(months)

    """Fill input widgets with default values """

    def fill_day(self):
        log.debug("event from %s", self.sender())
        self.ui.comboBox_Day.clear()
        self.month = self.ui.comboBox_Month.currentText()
        if self.month:
            days = self.filesAndDirs.get_days(int(self.year), int(self.month))
            if days:
                self.ui.comboBox_Day.addItems(days)

    """Update list of experiments """

    def fill_exp(self):
        log.debug("event from %s", self.sender())
        self.ui.comboBox_Exp.clear()
        self.day = self.ui.comboBox_Day.currentText()
        if self.day:
            self.directory = self.filesAndDirs.get_dirname(self.folder, int(self.year),
                                                           int(self.month), int(self.day))
            if self.directory:
                experiments = self.filesAndDirs.get_exp(self.directory)
                self.ui.comboBox_Exp.addItems(experiments)

    """Update list of spectra """

    def fill_spectra(self):
        log.debug("event from %s", self.sender())
        self.ui.comboBox_Number.clear()
        self.exp = self.ui.comboBox_Exp.currentText()
        if self.exp:
            numbers = self.filesAndDirs.get_spectra(self.directory, self.exp)
            if numbers:
                self.ui.comboBox_Number.addItems(numbers)

    def emit_signals(self):
        log.debug("event from %s", self.sender())
        self.number = self.ui.comboBox_Number.currentText()
        if self.number:
            spectrum_name = self.filesAndDirs.get_spectrumName(
                self.directory, self.exp, self.number)
            self.analysisRaisedSignal.emit(spectrum_name)
            self.masstabRaisedSignal.emit(spectrum_name)
        else:
            log.error("No data, accumulation not selected")

if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
