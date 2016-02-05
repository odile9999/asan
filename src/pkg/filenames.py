#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
This module manages the PIRENEA filenames.
"""
import os
import logging
log = logging.getLogger('root')


class FilesAndDirs(object):

    """
    Manage to find spectra in data directories
    """

    def __init__(self, folder="G:", year=2015, month=5, day=12):
        """
        Constructor
        """
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.folder = folder + os.sep + "HASSAN" + \
            os.sep + "Aroma" + os.sep + "Spectra"
        self.files = []

    def get_years(self, folder):
        """
        Returns a list of years, for one folder
        """
        self.folder = folder
        dirname = os.path.abspath(self.folder)
        list_years = []

        if not os.path.isdir(dirname):
            log.error("Not a directory: %s", dirname)
        else:
            li = os.listdir(dirname)
            for y in li:
                if (len(y) == 10):
                    list_years.append(y[0:4])
            list_years = list(dict().fromkeys(list_years).keys())
            list_years.sort()

        return list_years

    def get_months(self, year):
        """
        Return a list of months for one directory
        """
        self.year = year
        dirname = os.path.abspath(self.folder)
        list_months = []

        if not os.path.isdir(dirname):
            log.error("Not a directory: %s", dirname)
        else:
            mo = os.listdir(dirname)
            for m in mo:
                if (len(m) == 10):
                    if (m[0:4] == ('%02d' % self.year)):
                        list_months.append(m[5:7])
            list_months = list(dict().fromkeys(list_months).keys())
            list_months.sort()

        return list_months

    def get_days(self, year, month):
        """
        Return a list of spectrum numbers for one directory
        """
        self.year = year
        self.month = month
        dirname = os.path.abspath(self.folder)
        list_days = []

        if not os.path.isdir(dirname):
            log.error("Not a directory: %s", dirname)
        else:
            di = os.listdir(dirname)
            for d in di:
                if (len(d) == 10):
                    if (d[0:4] == ('%02d' % self.year) and d[5:7] == ('%02d' % self.month)):
                        list_days.append(d[8:])
            list_days = list(dict().fromkeys(list_days).keys())
            list_days.sort()

        return list_days

    def get_dirname(self, folder, year, month, day):
        """
        Return a full path name of one directory
        """
        self.folder = folder
        self.year = year
        self.month = month
        self.day = day

        # create directory name
        directory = '%d' % self.year + \
            "-" + '%02d' % self.month + \
            "-" + '%02d' % self.day

        dirname = os.path.join(self.folder, directory)

        return dirname

    def get_exp(self, dirname):
        """
        Return a list of experiments for one day
        """
        list_exp = []
        if not os.path.isdir(dirname):
            log.error("Not a directory: %s", dirname)
        else:
            self.files = os.listdir(dirname)
            for f in self.files:
                if (f.endswith(".txt")):
                    list_exp.append(f[:f.rfind("_")])
            """ remove duplicate names and sort the lists """
            list_exp = list(dict().fromkeys(list_exp).keys())
            list_exp.sort()

        return list_exp

    def get_spectra(self, dirname, exp):
        """
        Return a list of spectrum numbers for one directory
        """
        spectra = []

        if not os.path.isdir(dirname):
            log.error("Not a directory: %s", dirname)
        else:
            self.files = os.listdir(dirname)
            for f in self.files:
                if (f[:f.rfind("_")] == exp):
                    spectra.append(f[f.rfind("_") + 1:].split(sep='.')[0])
            """ remove duplicate names and sort the lists """
            spectra = list(dict().fromkeys(spectra).keys())
            """ sort list of strings as it was a list of numbers : 12 is after 2 """
            spectra = sorted(spectra, key=int)

        return spectra

    def get_spectrumName(self, dirname, exp, specNum):
        """
        Return a spectrum name from a given directory, number, acquis, accum
        """
        spectrumName = ""

        if not os.path.isdir(dirname):
            log.error("Not a directory: %s", dirname)
        else:
            # create spectrum name
            spectrumName = dirname + os.sep + \
                str(exp) + str("_") + \
                '%d' % int(specNum) + str(".txt")

        return spectrumName

if __name__ == '__main__':
    """ test within one directory """
#     folder = input("Root directory for data (G:\PIRENEA_manips):")
#     year = input("Year (2014):")
#     month = input("Month (5):")
#     day = input("Day (12):")
    fi = FilesAndDirs("G:\PIRENEA_manips", 2014, 5, 12)
    years = fi.get_years("G:\PIRENEA_manips")
    print("years=", years)
    directory = "G:\PIRENEA_manips\\2014\\data_2014_05_12"
    spectra = fi.get_spectra(directory)
    print("spectra=", spectra)
    acquis = fi.get_acquis(directory, "001")
    accums = fi.get_accums(directory, "001", "A")
    print("acq=", acquis, "acc=", accums)
    specName = fi.get_spectrumName(directory, 2014, 5, 12, 1, str("A"), 1)
    print("name = ", specName)

else:
    log.info("Importing... %s", __name__)
