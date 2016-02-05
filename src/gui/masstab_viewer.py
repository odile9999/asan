#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
This module manages the GUI of the masstab viewer.
"""
import os

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtWidgets import QFileDialog

from gui.masstab_viewer_qt import Ui_DockWidget_MassTabViewer
from pkg.peaks import Peaks
import logging
log = logging.getLogger('root')


class MassTabViewerGUI(QDockWidget):

    """
    classdocs
    """

    """ constructor """

    def __init__(self, parent=None):
        super(MassTabViewerGUI, self).__init__(parent)
        self.ui = Ui_DockWidget_MassTabViewer()
        self.ui.setupUi(self)

    def setup(self, masstab_selector, analysis):
        self.ms = masstab_selector
        self.ana = analysis
        self.mass_list = []
        self.dir_name = ""
        self.short_name = ""
        self.clear_text()
        self.__connect_events()

    def __connect_events(self):
        self.ms.masstabViewRaisedSignal.connect(self.update_columns)
        self.ana.masstabRaisedSignal.connect(self.update_filename)
        self.ui.pushButton_Clear.clicked.connect(self.clear_text)
        self.ui.pushButton_Automatic.clicked.connect(self.automatic_fill)
        self.ui.pushButton_Write.clicked.connect(self.write_file)
        self.ui.doubleSpinBox_Accuracy.setValue(0.2)
        self.ui.doubleSpinBox_Accuracy.valueChanged.connect(self.acc_event)

    def acc_event(self):
        log.debug("event from %s", self.sender())
        self.acc = float(self.ui.doubleSpinBox_Accuracy.value())

    def update_columns(self, mass_list):
        log.debug("event from %s", self.sender())
        #         self.__clear_text()
        self.mass_list = sorted(mass_list)
        text = "\n" + " " * 21
        for mass in self.mass_list:
            text = text + str(mass).ljust(8)
        text = text + "\n" + "=" * 18
        self.ui.plainTextEdit_Viewer.appendPlainText(text)

    def update_filename(self, filename):
        log.debug("event from %s", self.sender())
        self.ui.pushButton_Automatic.setEnabled(True)
        self.ui.pushButton_Write.setEnabled(True)
        self.short_name = os.path.basename(filename)
        self.dir_name = os.path.dirname(filename)

    def clear_text(self):
        log.debug("event from %s", self.sender())
        self.spectrum_name = ""
        self.ui.plainTextEdit_Viewer.clear()

    def automatic_fill(self):
        log.debug("event from %s", self.sender())
        if len(self.mass_list) == 0:
            return
        #         if self.ana.pip.signal is None:
        #             return
        x = self.ana.pip.mass
        y = self.ana.pip.spectrum
        self.acc_event()
        p = Peaks()
        dict_peak = p.masstab_peaks(x, y, self.mass_list, self.acc)
        text = str(self.short_name).ljust(21)
        for mass in self.mass_list:
            text = text + "{:.3f}".format(float(dict_peak[mass])).ljust(8)
        self.ui.plainTextEdit_Viewer.appendPlainText(text)

    def write_file(self):
        log.debug("event from %s", self.sender())
        #         if self.dir_name:
        filename = QFileDialog.getSaveFileName(
            self, 'MassTab File', self.dir_name, filter='masstab*.txt')
        if filename:
            with open(filename, mode="w", encoding='utf_8') as file:
                file.write(self.ui.plainTextEdit_Viewer.toPlainText())


if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
