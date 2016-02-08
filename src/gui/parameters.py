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

from gui.parameters_qt import Ui_DockWidget_Parameters
import logging
log = logging.getLogger('root')


class ParametersGUI(QDockWidget):

    """
    classdocs
    """

    """ constructor """

    def __init__(self, parent=None):
        super(ParametersGUI, self).__init__(parent)
        self.ui = Ui_DockWidget_Parameters()
        self.ui.setupUi(self)

    """ connect to events emitted by the data_selector """

    def setup(self, analysis):
        self.ana = analysis
        self.ana.parametersRaisedSignal.connect(self.fill_params)

    def fill_params(self, filename, pipeline):
        log.debug("event from %s", self.sender())
        short = str(filename).split(sep="\\")
        self.ui.lineEdit_Date.setText(short[-1])

        if pipeline.raw.scriptable:
            self.enable_parameters_box()
            self.script = pipeline.scr
            self.update_header()
        else:
            self.disable_parameters_box()

    def enable_parameters_box(self):
        self.ui.label_Date.setVisible(True)
        self.ui.lineEdit_Date.setVisible(True)
        self.ui.label_Header.setVisible(True)
        self.ui.plainTextEdit_Header.setVisible(True)

    def disable_parameters_box(self):
        self.ui.label_Date.setVisible(False)
        self.ui.lineEdit_Date.setVisible(False)
        self.ui.label_Header.setVisible(False)
        self.ui.plainTextEdit_Header.setVisible(False)

    def update_header(self):
        self.ui.lineEdit_Date.clear()
        self.ui.textEdit_Header.clear()
        self.ui.plainTextEdit_Header.set_text("toto")


if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)