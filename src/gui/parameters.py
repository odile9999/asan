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
        shortname = str(filename).split(sep="\\")
        self.ui.lineEdit_File.setText(shortname[-1])

        self.pip = pipeline
        self.update_header()

    def update_header(self):
        #         self.ui.plainTextEdit_Header.clear()
        self.ui.plainTextEdit_Header.setPlainText(self.pip.data.headtext)

if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
