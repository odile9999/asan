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


class AlyxanRawDataset(object):

    """
    Manage PIRENEA binary AlyXan files (little-endian).

    :Example:
    >>> import Signal
    >>> s = Signal()
    >>> s.read("signal.dat")
    >>> print (s.data[0:3])
    >>> print (s.step)
    [0.147, 0.148, 0.146]
    0.1
    """

    def __init__(self):
        """
        Constructor
        """
        self.filename = ""

    def read(self, filename=""):
        """
        Read a PIRENEA AlyXan binary file, in little-endian format.
        Populate data[] with the raw signal values and stepTime in seconds.

        :param filename: the name of the binary file to read
        """
        self.filename = filename
        data = []
        step = 0.0

        try:
            file = open(self.filename, mode="rb")
            # Read the first 4 bytes and convert to Int = number of points
            contents = file.read(4)
            points = struct.unpack('i', contents)[0]
            # Read all data points as float
            contents = file.read(4 * points)
            for i in range(points):
                data.append(struct.unpack('f', contents[i * 4:(i + 1) * 4])[0])
            # Read stepTime as double in seconds !!
            contents = file.read(8)
            step = struct.unpack('d', contents[0:8])[0] / 1000000.0
            file.close()

            return step, data

        except (IOError) as error:
            log.error("Unable to open : %s", error)
        except (struct.error) as error:
            log.error("Not a valid binary file : %s", error)


class RawDataset(object):

    """
    Manage PIRENEA old files (big-endian).

    :Example:

    >>> from pkg1.Dataset import RawDataset
    >>> s = RawDataset()
    >>> s.read("G:\\DATA_PIRENEA_OLD\\2014\\data140626\\26_06_2014_001.A00")
    >>> print ("Number of points: ", len(s.data))
    Number of points:  524288
    >>> print ("Step time: ", s.step)
    Step time:  5e-07
    """

    def __init__(self, filename=""):
        """
        Constructor
        """
        self.filename = filename
        self.points = 0
        self.signal = []
        self.step = 0.0
        self.start = 0
        self.end = 0
        self.scriptable = False

        self.__read_file()
#         self.__find_limits()

    def __read_file(self):
        """
        Read a PIRENEA OLD binary file, in big-endian format.
        Populate signal[] with the raw signal values and stepTime in seconds.
        """
        try:
            # Read first integer with number of points
            dt = np.dtype([('points', '>i4')])
            data = np.fromfile(self.filename, dtype=dt, count=1)
            self.points = int(data['points'])
            # Setup format of the binary part and read it (from is faster)
            dt = np.dtype(
                [('points', '>i4'), ('samples', '>f', (self.points,)), ('step', '>f')])
            data = np.fromfile(self.filename, dtype=dt)
            self.signal = data['samples'].ravel()
            self.step = float(data['step']) * 1e-6  # step in microseconds
            # Skip the binary part and read the script (readlines is faster)
            with open(self.filename, mode="rb") as fir:
                fir.read(4 + (4 * self.points) + 4)
                self.text = fir.readlines()

#             with open(self.filename, mode="rb") as fir:
# Read the first 4 bytes and convert to Integer to get the
# number of points """
#                 t = time.time()
#
#                 contents = fir.read(4)
#                 self.points = struct.unpack('>i', contents)[0]
#
# Read all data points as floats """
#                 contents = fir.read(4 * self.points)
#
# Fill data with empty values, faster than append """
#                 t = time.time()
#                 signal = self.points * [0.0]
#                 t1 = time.time() - t
#                 t = time.time()
#                 for i in range(self.points):
#                     signal[i] = struct.unpack(
#                         '>f', contents[i * 4:(i + 1) * 4])[0]
# self.signal = np.asarray(signal)
#                 t2 = time.time() - t
#                 self.signal = signal
# Read stepTime as float in seconds """
#                 contents = fir.read(4)
#                 self.step = struct.unpack('>f', contents)[0] / 1000000.0
#
#                 """ Read the script in text format and save it """
# Use readlines and NOT readline otherwise first line is
# missing """
#                 t = time.time()
#                 self.text = fir.readlines()
#                 t3 = time.time() - t
#             print("time readfile", t1, t2, t3)

            if len(self.text) > 0:
                self.scriptable = True
                if os.path.isfile(self.filename + "_sc.txt"):
                    pass
                else:
                    with open(self.filename + "_sc.txt", mode="w", encoding='utf_8') as file:
                        log.info("Script file creation...")
                        for line in self.text:
                            # strip removes all whitespace characters
                            if line.strip():
                                linew = line.decode('utf_8')
                                if linew[0] != '/' and linew[0] != '':
                                    file.write(linew)
            else:
                self.scriptable = False

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
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_07_30\\2014_07_30_001.A00"
#     filename = "D:\\PIRENEA_manips\\data140515\\15_05_2014_001.A00"
#     filename = "G:\\DATA_PIRENEA_OLD\\DATA_2014\\data140515\\15_05_2014_001.A00"
    raw = RawDataset(filename)
    points = len(raw.signal)
    print("Number of points: ", points)
    print("Step time: ", raw.step)
    print("first points", raw.signal[0:8])
    print("last points", raw.signal[524280:])

#     file = open(filename, 'rb')
#     header = file.read(149)
#     contents = file.read(4)
#     points = struct.unpack('>i', contents)[0]

    dt = np.dtype([('points', '>i4')])
    data = np.fromfile(filename, dtype=dt, count=1)
    points = data['length'].ravel()
    print("dt points: ", points, type(points))
    t = time.time()
    dt = np.dtype(
        [('length', '>i4'), ('samples', '>f', (points,)), ('step', '>f')])
    data = np.fromfile(filename, dtype=dt)
    # NB: count can be omitted -- it just reads the whole file then
    signal = data['samples'].ravel()
    step = data['step'].ravel()
    t1 = time.time() - t

    print("type de series", type(signal), len(signal))
    print("val first", signal[0:10])
    print("setp ", step, type(step))
    print("time", t1)

    t = time.time()
    with open(filename, mode="rb") as fir:
        contents = fir.read(4 + (4 * points) + 4)
        text = fir.readlines()
    t1 = time.time() - t
    print("time script", t1)


#         import matplotlib.pyplot as plt
#         xpoints = num.arange(len(raw.signal))
#         plt.plot(xpoints, raw.signal)
#         plt.show()
#
#         raw.truncate(raw.start, np.round(len(raw.signal) / 2))
#
#         xpoints = num.arange(len(raw.truncated))
#         plt.plot(xpoints, raw.truncated)
#         plt.show()

else:
    log.info("Importing... %s", __name__)
