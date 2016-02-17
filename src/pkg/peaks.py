#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
Detect peaks automatically.
Picked up from internet.

"""
import numpy as np
import logging
log = logging.getLogger('root')


class Peaks(object):

    """
    classdocs
    """

    def __init__(self, x=[], y=[]):
        """
        Constructor
        """
        self.x = x
        self.y = y

    def detect_peaks(self, x, mph=1.0, mpd=1, threshold=0, edge='rising',
                     kpsh=False, valley=False, show=False):
        """Detect peaks in data based on their amplitude and other features.

        Parameters
        ----------
        x : 1D array_like
            data.
        mph : {None, number}, optional (default = None)
            detect peaks that are greater than minimum peak height.
        mpd : positive integer, optional (default = 1)
            detect peaks that are at least separated by minimum peak distance (in
            number of data).
        threshold : positive number, optional (default = 0)
            detect peaks (valleys) that are greater (smaller) than `threshold`
            in relation to their immediate neighbors.
        edge : {None, 'rising', 'falling', 'both'}, optional (default = 'rising')
            for a flat peak, keep only the rising edge ('rising'), only the
            falling edge ('falling'), both edges ('both'), or don't detect a
            flat peak (None).
        kpsh : bool, optional (default = False)
            keep peaks with same height even if they are closer than `mpd`.
        valley : bool, optional (default = False)
            if True (1), detect valleys (local minima) instead of peaks.
        show : bool, optional (default = False)
            if True (1), plot data in matplotlib figure.
        ax : a matplotlib.axes.Axes instance, optional (default = None).

        Returns
        -------
        ind : 1D array_like
            indeces of the peaks in `x`.

        Notes
        -----
        The detection of valleys instead of peaks is performed internally by simply
        negating the data: `ind_valleys = detect_peaks(-x)`

        The function can handle NaN's

        See this IPython Notebook [1]_.

        References
        ----------
        .. [1] http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb

        Examples
        --------
        >>> from detect_peaks import detect_peaks
        >>> x = np.random.randn(100)
        >>> x[60:81] = np.nan
        >>> # detect all peaks and plot data
        >>> ind = detect_peaks(x, show=True)
        >>> print(ind)

        >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
        >>> # set minimum peak height = 0 and minimum peak distance = 20
        >>> detect_peaks(x, mph=0, mpd=20, show=True)

        >>> x = [0, 1, 0, 2, 0, 3, 0, 2, 0, 1, 0]
        >>> # set minimum peak distance = 2
        >>> detect_peaks(x, mpd=2, show=True)

        >>> x = np.sin(2*np.pi*5*np.linspace(0, 1, 200)) + np.random.randn(200)/5
        >>> # detection of valleys instead of peaks
        >>> detect_peaks(x, mph=0, mpd=20, valley=True, show=True)

        >>> x = [0, 1, 1, 0, 1, 1, 0]
        >>> # detect both edges
        >>> detect_peaks(x, edge='both', show=True)

        >>> x = [-2, 1, -2, 2, 1, 1, 3, 0]
        >>> # set threshold = 2
        >>> detect_peaks(x, threshold = 2, show=True)
        """
        x = np.atleast_1d(x).astype('float64')
        if x.size < 3:
            return np.array([], dtype=int)
        if valley:
            x = -x
        # find indices of all peaks
        dx = x[1:] - x[:-1]
        # handle NaN's
        indnan = np.where(np.isnan(x))[0]
        if indnan.size:
            x[indnan] = np.inf
            dx[np.where(np.isnan(dx))[0]] = np.inf
        ine, ire, ife = np.array([[], [], []], dtype=int)
        if not edge:
            ine = np.where(
                (np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) > 0))[0]
        else:
            if edge.lower() in ['rising', 'both']:
                ire = np.where(
                    (np.hstack((dx, 0)) <= 0) & (np.hstack((0, dx)) > 0))[0]
            if edge.lower() in ['falling', 'both']:
                ife = np.where(
                    (np.hstack((dx, 0)) < 0) & (np.hstack((0, dx)) >= 0))[0]
        ind = np.unique(np.hstack((ine, ire, ife)))
        # handle NaN's
        if ind.size and indnan.size:
            # NaN's and values close to NaN's cannot be peaks
            ind = ind[np.in1d(
                ind, np.unique(np.hstack((indnan, indnan - 1, indnan + 1))), invert=True)]
        # first and last values of x cannot be peaks
        if ind.size and ind[0] == 0:
            ind = ind[1:]
        if ind.size and ind[-1] == x.size - 1:
            ind = ind[:-1]
        # remove peaks < minimum peak height
        if ind.size and mph is not None:
            ind = ind[x[ind] >= mph]
        # remove peaks - neighbors < threshold
        if ind.size and threshold > 0:
            dx = np.min(
                np.vstack([x[ind] - x[ind - 1], x[ind] - x[ind + 1]]), axis=0)
            ind = np.delete(ind, np.where(dx < threshold)[0])
        # detect small peaks closer than minimum peak distance
        if ind.size and mpd > 1:
            ind = ind[np.argsort(x[ind])][::-1]  # sort ind by peak height
            idel = np.zeros(ind.size, dtype=bool)
            for i in range(ind.size):
                if not idel[i]:
                    # keep peaks with the same height if kpsh is True
                    idel = idel | (ind >= ind[i] - mpd) & (ind <= ind[i] + mpd) \
                        & (x[ind[i]] > x[ind] if kpsh else True)
                    idel[i] = 0  # Keep current peak
            # remove the small peaks and sort back the indices by their
            # occurrence
            ind = np.sort(ind[~idel])

        if show:
            if indnan.size:
                x[indnan] = np.nan
            if valley:
                x = -x
            print("no plot, sorry")

        return ind

    def prepare_detect(self, ref, accuracy, xx, yy, startx, endx):
        # search values to detect peaks around a central value
        m = ref
        a = accuracy
        x = np.asarray(xx)
        y = np.asarray(yy)
        mask1 = [(x >= m) & (x <= m + a)]
        # Minimum peak distance (to avoid edge peaks of same peak)
        mpd = len(x[mask1]) / 1.5
        # create a mask for start to end values
        mask = [(x >= (startx)) & (x <= (endx))]
        # minimum peak height (to avoid peaks of noise)
#         mph = np.average(y[mask]) * 5.0
        # By default choose average OR max / 50.0
        mph = np.max(y[mask]) / 50.0

        return mph, mpd, mask

    def masstab_peaks(self, xx, yy, ind_list, accuracy=0.2):
        res_m = {}
        res_i = {}
        x = np.asarray(xx)
        y = np.asarray(yy)
        a = accuracy
        for dummy, index in enumerate(ind_list):
            m = float(index)
            mask = [(x >= m - a) & (x <= m + a)]
            # process peaks around a mass value
            if len(y[mask]) > 0:
                # find max value = peak
                peak = max(y[mask])
                # find exact mass corresponding to the peak
                val = [i for i, j in enumerate(y[mask]) if j == peak]
                res_m[index] = x[mask][val]
                res_i[index] = y[mask][val]
            else:
                res_m[index] = 0.0
                res_i[index] = 0.0

        return res_m, res_i

    def get_peaks(self, x, y, startx, endx, mph_in=0.0, mpd_in=0):
        log.info("enter")
        ref = startx + (abs(endx - startx) / 2)
        delta = 1.0
        mph_o, mpd_o, mask = self.prepare_detect(
            ref, delta, x, y, startx, endx)

        if mph_in > 0.0:
            mph = mph_in
        else:
            mph = mph_o
        if mpd_in > 0:
            mpd = mpd_in
        else:
            mpd = mpd_o

        xx = np.asarray(x)
        yy = np.asarray(y)
        # Detect peak on rising edge
        edge = 'rising'
        # Detect peak greater than threshold
        threshold = 0.0
        y = yy[mask]
        x = xx[mask]
        ind = self.detect_peaks(y, mph, mpd, threshold, edge)
#         print("here is mph mpd:", mph, mpd, ind, x[ind], y[ind])
#         print("here is mpho mpdo:", mph_o, mpd_o, ind)

        return mph_o, mpd_o, mask, ind


if __name__ == '__main__':

    import matplotlib.pyplot as plt
    from pkg.dataset import Dataset

    filename = "G:\\HASSAN\\Aroma\\Spectra\\2016-01-28\\Cor_1.txt"
#     filename = "G:\\HASSAN\\Aroma\\Spectra\\2016-01-28\\HS_mix_1.txt"
    raw = Dataset(filename)

    x = np.asarray(raw.mass)
    y = np.asarray(raw.spectrum)

    plt.plot(x, y)

    ref_mass = 300.0
    delta = 20.0
    startx = ref_mass - delta / 2
    endx = ref_mass + delta / 2
    accuracy = 1.0
    p = Peaks()

    mph, mpd, mask = p.prepare_detect(ref_mass, accuracy, x, y, startx, endx)
    print("type mask", type(mask))
    print("mph=", mph, " mpd=", mpd)
    # Detect peak on rising edge
    edge = 'rising'
    # Detect peak greater than threshold
    threshold = 0.0
    # Don't use default plot
    mph = 400.0
    mpd = 50
    print(y[mask][0])

    ind = p.detect_peaks(y[mask], mph, mpd, threshold, edge)
    print("type ind", type(ind))
    print("mass =", x[mask][ind])
    print("inten=", y[mask][ind])

    fig, ax = plt.subplots(1, 1)
    line1, = ax.plot(x[mask], y[mask], 'b', lw=1)

    line2, = ax.plot(
        x[mask][ind], y[mask][ind], '+', mfc=None, mec='r', mew=2, ms=8)

    ax.set_title("%s (mph=%.3f, mpd=%d, threshold=%s, edge='%s')"
                 % ('Peak detection', mph, mpd, str(threshold), edge))
    # test legende
    # fig.legend([line2], ['nnn'])

    # test annotations
    x = x[mask][ind]
    y = y[mask][ind]
    for i, j in zip(x, y):
        #     ax.annotate(str(j), xy=(i, j))
        ax.annotate("{:.3f}".format(float(j)), xy=(i, j))

    plt.show()

else:
    log.info("Importing... %s", __name__)
