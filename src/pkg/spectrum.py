#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
Process mass for AROMA specyra.
"""


class Spectrum(object):
    """
    Process a mass spectrum from ToF AROMA data
    """

    def __init__(self):
        """
        Constructor
        """

        self.time = []
        self.spectrum = []

#         self.process_mass()

    def fit_func(self, x, a, b, c):
        """
        Function of type a*x**2 + b*x +c
        """
        return a * x**2 + b * x + c


if __name__ == '__main__':
    #     import numpy as np
    #     from scipy.optimize import curve_fit
    #     import matplotlib.pyplot as plt
    #     from pkg.dataset import Dataset
    #
    #     #     from pkg1.dataset import AlyxanRawDataset
    #     filename = "G:\\HASSAN\\Aroma\\Spectra\\2016-01-28\\Cor_1.txt"
    #
    #     sp = Spectrum()
    #
    #     x = np.array([1, 2, 3, 9])
    #     y = np.array([1, 4, 1, 3])
    #
    #     params = curve_fit(sp.fit_func, x, y)
    #
    # #     [a, b, c] = params[0]
    #     print("paramas", params[0])
    from pkg.dataset import Dataset
    import numpy as np
    import matplotlib.pyplot as plt

    points = np.array([(1, 1), (2, 4), (3, 1), (9, 3)])
    # valeurs prises dans un fichier déjà calibré, pour vérif
    # attention ! valeur 0 obligatoire sinon le fit ne converge pas
    x = [0.0, 20039.0, 30409.0, 35859.0, 35980.0]
    y = [0.001, 94.36474, 215.00997, 298.0274, 300.0228]

    # ordre du polynome 2 : ax2 + bx + c
    # si ordre 3 donne de meilleurs résultats
    coefs, stats = np.polynomial.polynomial.polyfit(x, y, 3, full=True)
    print("coefs =", coefs)
    print("stats = si faible OK", stats)
#     ffit = np.polynomial.polynomial.Polynomial(coefs)
#     print("ffit", type(ffit))

    filename = "G:\\HASSAN\\Aroma\\Spectra\\2016-01-28\\Cor_1.txt"
    raw = Dataset(filename)

    x_new = np.asarray(raw.time)
    y_new = np.asarray(raw.spectrum)
    ffit = np.polynomial.polynomial.polyval(x_new, coefs)
    # courbe pour montrer le fit sur 4 points
    plt.plot(y, x, 'o', ffit, x_new)
    # courbe de masse calibrée
    plt.plot(ffit, y_new)
#     plt.plot(ffit(x_new), y_new)
    plt.show()

#     plt.plot(x, y, 'o', x_new, ffit(x_new))
#     plt.plot(x_new, y_new)
#     plt.plot(x_new, ffit(x_new))

#     # calculate polynomial
#     z = np.polyfit(x, y, 3)
#     f = np.poly1d(z)
#     print("f=", f)
#
#     # calculate new x's and y's
#     x_new = np.linspace(x[0], x[-1], 50)
#     print(type(x_new))
#     y_new = f(x_new)
#
#     plt.plot(x, y, 'o', x_new, y_new)
#     plt.xlim([x[0] - 1, x[-1] + 1])
#     plt.show()
# #     filename = "G:\\HASSAN\\Aroma\\Spectra\\2016-01-28\\HS_mix_1.txt"
#     raw = Dataset(filename)
#
#     x = np.asarray(raw.mass)
#     y = np.asarray(raw.spectrum)
#
#     plt.plot(x, y)
