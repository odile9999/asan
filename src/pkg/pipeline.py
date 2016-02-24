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
        self.data = Dataset(self.filename)

    def find_calib(self, time_list, mass_list):
        self.time_list = time_list
        self.mass_list = mass_list
        print("time_list= ", time_list)
        print("mass_list= ", mass_list)
        # ordre du polynome 2 : ax2 + bx + c
        # si ordre 3 donne de meilleurs résultats
        coefs, stats = np.polynomial.polynomial.polyfit(time_list, mass_list, 3, full=True)
        print("coefs =", coefs, len(coefs))
        print("stats = si faible OK", stats)
    #     ffit = np.polynomial.polynomial.Polynomial(coefs)
    #     print("ffit", type(ffit))
        return coefs

    def calib_mass(self, coefs):
        print("cali_mass ENTER")
        mass = np.polynomial.polynomial.polyval(self.data.time, coefs)
        self.data.update_mass(mass)
        print("cali_mass, isCalibDone", self.data.isCalibDone)
#     plt.plot(y, x, 'o', ffit, x_new)
#     # courbe de masse calibrée
#     plt.plot(ffit, y_new)

    def process_peaks(self, xin, yin, mph=0.0, mpd=0, x1=0.0, x2=0.0):
        """
        Within a range of mass [x1, x2], get indices of maximum intensity (ind)
        with a peak height and a peak distance provided as input params (mph, mpd)
        suggested values are returned into mph_o, mpd_o, if needed
        ==> caution ! indices are from x[mask], not full x array
        """

        x = np.asarray(xin)
        y = np.asarray(yin)

        p = Peaks()

        mph_o, mpd_o, mask, ind = p.get_peaks(x, y, x1, x2, mph, mpd)

        xx = x[mask]
        yy = y[mask]

        return mph_o, mpd_o, xx, yy, xx[ind], yy[ind]

    def get_x1_x2_mass(self, xin, yin, mass_x1, mass_x2):

        x = np.asarray(xin)
        y = np.asarray(yin)
        mask = [(x >= mass_x1) & (x <= mass_x2)]

        return x[mask], y[mask]

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
