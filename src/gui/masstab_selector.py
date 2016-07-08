#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
This module manages the GUI of the masstab selector.
"""
from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt

from gui.masstab_selector_qt import Ui_DockWidget_MassTabSelector
import logging
log = logging.getLogger('root')


class MassTabSelectorGUI(QDockWidget):

    """
    classdocs
    """
    masstabViewRaisedSignal = pyqtSignal(object)

    """ constructor """

    def __init__(self, parent=None):
        super(MassTabSelectorGUI, self).__init__(parent)
        self.ui = Ui_DockWidget_MassTabSelector()
        self.ui.setupUi(self)

    def setup(self, analysis):
        self.ana = analysis
        self.__connect_events()

    def __connect_events(self):
        self.model = QStandardItemModel()
        self.mass_list = []
        for i in range(10):
            mass = 184 + i
            self.mass_list.append(str(mass))
        for i in range(10):
            mass = 209 + i
            self.mass_list.append(str(mass))
        for i in range(10):
            mass = 273.3 + i
            self.mass_list.append(str(mass))
        for i in range(10):
            mass = 294 + i
            self.mass_list.append(str(mass))
        for mass in self.mass_list:
            item = QStandardItem(mass)
            item.setCheckable(True)
            item.setEditable(True)
            self.model.appendRow(item)
        self.view = self.ui.listView_Mass
        self.view.setModel(self.model)
        # changes in one item, don't know which one
        self.model.itemChanged.connect(self.change_list)
        # changes in button
        self.ui.pushButton_ChangeList.clicked.connect(self.emit_list_signal)
        # get peaks found and update automatically the mass list
        self.ana.masstabSelectorRaisedSignal.connect(self.update_list_view)

    def update_list_view(self, xind):
        self.mass_list = []
        for i in range(len(xind)):
            m = "{:.1f}".format(float(xind[i]))
            self.mass_list.append(str(m))
        self.model.clear()
        self.model = QStandardItemModel()

        for mass in self.mass_list:
            item = QStandardItem(mass)
            item.setCheckable(True)
            item.setEditable(True)
            item.setCheckState(Qt.Checked)
            self.model.appendRow(item)
        self.view = self.ui.listView_Mass
        self.view.setModel(self.model)
        # changes in one item, don't know which one
        self.model.itemChanged.connect(self.change_list)

    def change_list(self):
        log.debug("event from %s", self.sender())
        self.oneIsChecked = False
        self.mass_list = []
        count = self.model.rowCount()
        for i in range(count):
            checked = self.model.item(i).checkState()
            if checked:
                mass_name = self.model.data(self.model.index(i, 0))
                self.mass_list.append(mass_name)
                self.oneIsChecked = True

    def emit_list_signal(self):
        log.debug("event from %s", self.sender())
        self.change_list()
        if self.oneIsChecked:
            self.masstabViewRaisedSignal.emit(self.mass_list)


if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
