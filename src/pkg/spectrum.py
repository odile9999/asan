#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
Process mass and frequency spectra on PIRENEA data.
"""
import os
from scipy import constants
import numpy as np
import logging
log = logging.getLogger("root")


class FrequencySpectrum(object):

    """
    Process a Frequency Spectrum from a PIRENEA signal and stepTime in seconds.
    """

    def __init__(self, signal=[], stepTime=0.0):
        """
        Constructor
        """
        self.freq = []
        self.spectrum = []
        self.powerSpectrum = []
        self.signal = signal
        self.stepTime = stepTime

        self.__calculate_spectrum()

    def __calculate_spectrum(self):
        """
        Process a single sided amplitude frequency spectrum of signal(t).

        Populate spectrum[] with amplitude frequency spectrum of signal(t).
        Populate freq[] with frequency steps in Hz from stepTime in seconds.
        :param signal: signal(t)
        :param stepTime: stepTime in seconds
        """
        n = len(self.signal)
        """One side spectrum of real part only """
        y = np.fft.rfft(self.signal) / n
        f = np.fft.rfftfreq(n, self.stepTime)
        self.spectrum = np.abs(y)
        self.freq = f
        self.powerSpectrum = np.abs(self.spectrum) ** 2

    def write_to_textFile(self, filename=""):
        """
        Writes a frequency spectrum to a file, in ASCII format.

        """
        self.filename = filename
        if os.path.isfile(self.filename + "_fsp.txt"):
            print("Frequency Spectrum ASCII file already exists")
        else:
            with open(self.filename + "_sp.txt", mode="w", encoding='utf_8') as file:
                n = len(self.spectrum)
                linew = str(n) + "\n"
                file.write(linew)
                for i in range(n):
                    linew = "{:.5E}".format(self.freq[i]) + "\t" + \
                            "{:.5E}".format(self.spectrum[i]) + "\n"
                    file.write(linew)


class MassSpectrum(object):

    """
    Process a Mass Spectrum from a PIRENEA signal.
    B0 = 5 T
    """

    def __init__(self, freq=[], ref_mass=300.0939, cyclo_freq=255.723e3, mag_freq=0.001e3):
        """
        Constructor
        mass = A/nu - B/(nu*nu) with :
        A = refMass * true cyclotron
        B = refMass * modified cyclotron * magnetron
        cyclotronFreq value : 255.724e3
        N. Bruneleau value : 255.710e3
        """
        self.f = freq
#         print("min_freq=", min(freq))
#         print("max_freq=", max(freq))
#         self.mass = len(self.f) * [0.0]
        self.mass = np.zeros(len(self.f))
        self.refMass = ref_mass
        self.cyclotronFreq = cyclo_freq
        self.magnetronFreq = mag_freq

        self.__autocalib_mass()

    def __autocalib_mass(self):
        """
        Process a mass spectrum from a frequency spectrum.

        Populate massSpectrum[].
        Populate mass[] with uma.
        """
        A = self.refMass * self.cyclotronFreq
        B = self.refMass * \
            (self.cyclotronFreq - self.magnetronFreq) * self.magnetronFreq
        maxMass = A * A / (4 * B)
        minFreq = 2 * B / A
#         print("type(minfreq) =", type(minFreq))
#         print("maxMass=", maxMass)

        self.mass += maxMass
        mask = [self.f > minFreq]
        self.mass[mask] = A / self.f[mask] - B / (self.f[mask] ** 2)

    def __uncalib_mass(self, freq):
        """
        Process a mass spectrum from a frequency spectrum.

        Populate massSpectrum[].
        Populate mass[] with uma.

        :param spectrum: frequency spectrum
        """
        n = len(freq)
        mass = []
        q = constants.codata.value('elementary charge')  # 1.602176565e-19 C
        uma = constants.codata.value(
            'atomic mass constant')  # 1.660538921e-27 kg
        B0 = 5  # 5 Tesla for PIRENEA
        print("q=", q, ", uma=", uma)
        for i in range(n):
            mass.append(q * B0 / (freq[i] * 2 * np.pi * uma))
        self.mass = mass

    def basic_recalibrate(self, ref_mass, accuracy):
        """ Basic auto calibration with a known reference mass. """
        xx = np.array(self.mass)
        r = ref_mass
        y = self.spectrum
        mask = [(xx > (r - accuracy)) & (xx < (r + accuracy))]
        maxy = max(y[mask])
        bad_mass = 0.0
        ind = 0
        for i, j in enumerate(y[mask]):
            if j == maxy:
                bad_mass = xx[mask][i]
                ind = i
                print("i, j, bad_mass", i, j, bad_mass)
        delta_mass = (ref_mass / bad_mass)
        print("bad, delta=", bad_mass, delta_mass)
        print("xx UNCORRECT", xx[mask][ind])
        xx = np.array(self.mass) * delta_mass
        print("xx correct", xx[mask][ind])
        self.mass = xx

    def write_to_textFile(self, filename=""):
        """
        Writes a mass spectrum to a file, in ASCII format.

        """
        self.filename = filename
        if os.path.isfile(self.filename + "_sp.txt"):
            print("Mass Spectrum ASCII file already exists")
        else:
            with open(self.filename + "_sp.txt", mode="w", encoding='utf_8') as file:
                n = len(self.mass)
                linew = str(n) + "\n"
                file.write(linew)
                for i in range(n):
                    linew = "{:.5E}".format(self.mass[i])
                    file.write(linew)


if __name__ == '__main__':
    #     from pkg1.dataset import AlyxanRawDataset
    from pkg.dataset import RawDataset
    import matplotlib.pyplot as plt

    """ Prepare Subplots """
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)

    # Read PIRENEA signal
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_07_30\\2014_07_30_001.A00"
    #     filename = "D:\\PIRENEA_manips\\data140515\\15_05_2014_001.A00"
    #     filename = "G:\\DATA_PIRENEA_OLD\\DATA_2014\\data140515\\15_05_2014_001.A00"
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_06_26\\2014_06_26_010.A00"
    raw = RawDataset(filename)
    points = len(raw.signal)
    start = raw.start
    end = raw.end
    step = raw.step
    raw.hann()

    raw.truncate(start, end)

    y1 = raw.signal[start:end]
    limit = end - start

    y2 = raw.truncated

#     y3 = raw.signal[start:]
#     y3[end - start:] = 0.0

    y = y2
    x = np.arange(len(y)) * step
    print("len signal x, y=", len(x), len(y))
    ax1.plot(x, y)
    ax1.set_xlabel("time(s)")

    # Real FFT on complete signal
    fs = FrequencySpectrum(y, step)
    y = fs.spectrum * 1000.0
    x = fs.freq / 1000.0            # in kHz
    print("points, len x, y", points, len(x), len(y))
    ax2.plot(x, y)
    ax2.set_xlabel('Freq (kHz)')
    ax2.set_ylabel('|rfft|')

#     Write to ASCII
#     fs.write_to_textFile(filename)

# Mass with approximative calibration
    # Calculate mass
    x = fs.freq
    ms = MassSpectrum(x, y)
    xx = np.array(ms.mass)
    print("freq=", x)
    print("mass=", xx)

    mask = [(xx > 280.0) & (xx < 310.0)]
    print("len ymask=", len(xx[mask]), len(y[mask]), y[mask][0])
    ax3.plot(xx[mask], y[mask])
    ax3.set_xlabel('mass (u.a.m.)')
    ax3.set_ylabel('|rfft|')

    # Truncate signal of excitation
#     so.hann()
#     y = so.data
#     y = y[2400:]
#     print ("len signal=", len(y))
#     x = np.arange(len(y)) * step
#     plt.subplot(2, 2, 3)
#     plt.plot(x, y)

    # Real FFT on signal, minus excitation
#     y = so.data
#     print ("len signal2=", len(y))
#     spec.calculate_FFT(y, step)
#     plt.subplot(2, 2, 4)
#     plt.plot(spec.freq / 1000.0, abs(spec.spectrum))
#     plt.xlabel('Freq (kHz)')
#     plt.ylabel('|rfft|')
    plt.show()

else:
    log.info("Importing... %s", __name__)
