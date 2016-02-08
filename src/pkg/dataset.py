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
        self.signal = []
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
                                self.time.append(line.split('|')[0].strip())
                                self.signal.append(line.split('|')[1].strip())
                                self.mass.append(line.split('|')[2].strip())
            print("calib : ", calibAvailable, "\ntext = ", self.scr)
            print("time", self.time[0:10])
            print("time", self.signal[0:10])
            print("time", self.mass[0:10])

        except (IOError) as error:
            log.error("Unable to open : %s", error)
        except (struct.error) as error:
            log.error("Not a valid binary file : %s", error)

    def __find_limits(self):
        """
        Find the beginning and the end of signal just after excitation buffer

        """
        # if script is available, get limits according excitation length
        if self.scriptable:
            s = Script(self.filename)
            duration = s.get_excit_duration()
            self.start = round(duration / self.step)
            self.end = round(self.points / 2)
        # if script is not available, fix arbitrary limits
        else:
            self.start = 0
            self.end = round(self.points / 2)

    def get_science(self):

        if not self.dataReady:
            log.error("Data NOT available, please read data first")

        return self.signal, self.step

    def truncate(self, start=0, end=0):
        """
        Truncate the signal before start to remove excitation

        :param start: first interesting point of signal

        """
        if start < end:
            self.start = start
        if end > 0:
            self.end = end
        truncated = self.signal[self.start:self.end]

        return truncated

    def hann(self, signal, half=False):
        """
        Apply a Hann windowing on raw signal, before FFT.

        """
        points = len(signal)

        # Hanning from Herschel (half window)"""
        # hann = 0.5 * (1.0 + cos ((PI*i) / channels))"""
        if half:
            iarr = num.arange(points) * math.pi / points
            iarr = 0.5 + 0.5 * math.cos(iarr)
        # Hanning from numpy (full window)"""
        else:
            iarr = np.hanning(points)
        hann = signal * iarr

        return hann

if __name__ == '__main__':

    """
    main method to avoid error messages in pylint.
    """
    filename = "G:\\HASSAN\\Aroma\\Spectra\\2016-01-29\\Cor_1.txt"
#     filename = "D:\\PIRENEA_manips\\data140515\\15_05_2014_001.A00"
#     filename = "G:\\DATA_PIRENEA_OLD\\DATA_2014\\data140515\\15_05_2014_001.A00"
    raw = Dataset(filename)

#     with open(filename + ".scr", mode="rt") as filer:
#         for line in filer:
#             print(line)
else:
    log.info("Importing... %s", __name__)
