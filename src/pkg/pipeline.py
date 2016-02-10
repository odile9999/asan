#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
Process PIRENEA data.
"""

import numpy as np
from pkg.dataset import Dataset
from pkg.peaks import Peaks
from pkg.script import Script
from pkg.spectrum import FrequencySpectrum
from pkg.spectrum import MassSpectrum
import logging
log = logging.getLogger("root")


class Pipeline(object):

    """
    classdocs
    """

    def __init__(self, filename=""):
        """
        Constructor
        """
        self.filename = filename
        self.__process_file()

    def __process_file(self):
        """ operations on files """
        data = Dataset(self.filename)
        if data.points > 0:
            self.spectrum = data.spectrum
            self.time = data.time
            self.mass = data.mass
            self.points = data.points
        self.headtext = data.headtext

    def process_peaks(self, mph=0.0, mpd=0, startx=0.0, endx=0.0):
        log.info("process_peaks")

        if mph > 0:
            self.mph = mph
        if mpd > 0:
            self.mpd = mpd

        x = self.mass
        y = self.spectrum
        p = Peaks()
        ref = startx + (abs(endx - startx) / 2)
        delta = 1.0

        mph, mpd, mask = p.prepare_detect(ref, delta, x, y, startx, endx)

        # Detect peak on rising edge
        edge = 'rising'
        # Detect peak greater than threshold
        threshold = 0.0
        # Don't use default plot
        # CAUTION !! y must be transformed in np.asarray !!
        y = np.asarray(self.spectrum)
        ind = p.detect_peaks(y[mask], self.mph, self.mpd, threshold, edge)

        self.mph = mph
        self.mpd = mpd
        self.mask = mask
        self.ind = ind

    def process_peaks2(self, mph=0.5, mpd=1, startx=0.0, endx=0.0):
        log.info("process_peaks2")

        x = self.mass
        y = self.spectrum

        p = Peaks()
        # Detect peak on rising edge
        edge = 'rising'
        # Detect peak greater than threshold
        threshold = 0.0

        mph, mpd, mask, ind = p.get_peaks(
            x, y, startx, endx, mph, mpd, threshold, edge)

        # Don't use default plot
        # CAUTION !! y must be transformed in np.asarray !!
        y = np.asarray(self.spectrum)
        ind = p.detect_peaks(y[mask], self.mph, self.mpd, threshold, edge)

        self.mph = mph
        self.mpd = mpd
        self.mask = mask
        self.ind = ind

if __name__ == '__main__':

    import matplotlib.pyplot as plt

    # step = 0.5 524288
    filename = "G:\\PIRENEA_manips\\2010\\data_2010_07_27\\2010_07_27_002.A00"
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_06_26\\2014_06_26_011.A00"
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_07_30\\2014_07_30_001.A00"
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_07_30\\2014_07_30_001.A00"
    filename = "G:\\PIRENEA_manips\\2010\\data_2010_07_27\\2010_07_27_002.A00"
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_05_12\\2014_05_12_005.A00"
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_06_26\\2014_06_26_011.A00"

    pip = Pipeline(filename)
    mask = pip.mask
    ind = pip.ind

    x = np.asarray(pip.ms.mass)
    y = np.asarray(pip.ms.spectrum)
    print("mass =", x[mask][ind])
    print("peak =", y[mask][ind])

    fig, ax = plt.subplots(1, 1)
    line1, = ax.plot(x[mask], y[mask], 'b', lw=1)

    line2, = ax.plot(
        x[mask][ind], y[mask][ind], '+', mfc=None, mec='r', mew=2, ms=8)

    ax.set_title("%s (mph=%.3f, mpd=%d)" %
                 ('Peak detection', pip.mph, pip.mpd))
    # test legende
    # fig.legend([line2], ['nnn'])

    # test annotations
    x = x[mask][ind]
    y = y[mask][ind]
    for i, j in zip(x, y):
        #     ax.annotate(str(j), xy=(i, j))
        ax.annotate(
            "{:.3f} - {:.4f}".format(float(j), float(i)), xy=(i, j), fontsize=8)

    plt.show()

else:
    log.info("Importing... %s", __name__)
