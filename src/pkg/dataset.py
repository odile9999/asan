#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
This module manages the PIRENEA raw datasets.
"""
import os.path
import struct
import time

from numpy.core import numeric as num
from numpy.core import umath as math

import numpy as np
from pkg.script import Script
import logging
log = logging.getLogger('root')


class Dataset(object):

    """
    Manage AROMA files (ASCII).

    :Example:

    """

    def __init__(self, filename=""):
        """
        Constructor
        """
        self.filename = filename
        self.points = 0
        self.spectrum = []
        self.time = []
        self.mass = []
        self.scr = []

        self.__read_file()
#         self.__find_limits()

    def __read_file(self):
        """
        Read an AROMA file in ASCII format.
        """
        try:
            with open(self.filename, mode='rt', encoding='utf_8') as filer:
                calibAvailable = False
                index = 0
                # with open(self.filename + ".txt", mode="w", encoding='utf_8')
                # as filew:
                for line in filer:
                    if line.strip():
                        if '|' not in line:
                            self.scr.append(filer.readline())
                            if '.mz' in line:
                                calibAvailable = True
                        else:
                            if calibAvailable:
                                #                                 self.time.append(line.split('|')[0].strip())
                                #                                 self.spectrum.append(line.split('|')[1].strip())
                                #                                 self.mass.append(line.split('|')[2].strip())
                                self.time.append(float(line.split('|')[0].strip()))
                                self.spectrum.append(float(line.split('|')[1].strip()))
                                self.mass.append(float(line.split('|')[2].strip()))
                                index += 1
                            else:
                                log.info("No calibration file for mass")
            self.points = index
            if index > 0:
                print("calib : ", calibAvailable, "\ntext = ", self.scr)
                print("time", self.time[0:10])
                print("time", self.spectrum[0:10])
                print("time", self.mass[0:10])
                print("points", self.points)

        except (IOError) as error:
            log.error("Unable to open : %s", error)
        except (struct.error) as error:
            log.error("Not a valid binary file : %s", error)

    def truncate(self, start=0, end=0):
        """
        Truncate the spectrum before start to remove excitation

        :param start: first interesting point of spectrum

        """
        if start < end:
            self.start = start
        if end > 0:
            self.end = end
        truncated = self.spectrum[self.start:self.end]

        return truncated


if __name__ == '__main__':

    """
    main method to avoid error messages in pylint.
    """
    filename = "D:\\HASSAN\\Aroma\\Spectra\\2016-01-22\\Cor_1.txt"
    raw = Dataset(filename)

else:
    log.info("Importing... %s", __name__)
