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

    def process_peaks(self, mph=0.0, mpd=0, x1=0.0, x2=0.0):
        log.info("enter")

        x = np.asarray(self.mass)
        y = np.asarray(self.spectrum)

        p = Peaks()

        mph_o, mpd_o, mask, ind = p.get_peaks(x, y, x1, x2, mph, mpd)

        self.mask = mask
        self.ind = ind

        return mph_o, mpd_o

    def get_x1_x2_mass(self, mass_x1, mass_x2):

        x = np.asarray(self.mass)
        y = np.asarray(self.spectrum)
        mask = [(x >= mass_x1) & (x <= mass_x2)]
#         print("xmask, ymask", x[mask], y[mask])
        return x[mask], y[mask]

    def get_mask_peaks(self):
        log.info("enter")

        x = np.asarray(self.mass)
        y = np.asarray(self.spectrum)
        xx = x[self.mask]
        yy = y[self.mask]

        return xx, yy, xx[self.ind], yy[self.ind]


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
