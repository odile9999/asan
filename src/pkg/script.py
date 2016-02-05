#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
Process PIRENEA scripts.
"""
import os.path
import logging
log = logging.getLogger("root")


class Script(object):

    """
    Class to manage old script files in text format.
    Extract useful parameters and fill an XML file with them
    """

    def __init__(self, filename=""):
        """
        Constructor
        """
        self.filename = filename
        self.excitBuffer = []
        self.excitation = []
        self.ejectBuffer = []
        self.ejection = []
        self.detectBuffer = []
        self.detection = []
        self.excitDuration = 0.0

        self.__find_buffers()

    def __find_buffers(self):
        """
        Retrieve excitation buffers from script file within a tuple
        """
        buffers = []
        excitbuf = []
        ejectbuf = []
        excit = []
        eject = []

        # Read txt file, if it has been previously created by a Dataset.read()
        # """
        if os.path.isfile(self.filename + "_sc.txt"):
            with open(self.filename + "_sc.txt", mode='rt', encoding='utf_8') as file:
                for line in file:
                    linew = line.split()
                    # find all buffers eject/excit
                    if line[0] == 'B' and len(linew) > 1:
                        buffers.append(line.split())
                        if ("eject" in line) or ("elect" in line):
                            ejectbuf.append(line.split())
                        else:
                            excitbuf.append(line.split())
                    # find the buffers used during the sequence
                    if len(linew) > 1 and linew[1] == "Detect":
                        self.detectBuffer.append(linew[2])
                        excit.append(linew[2])

                    if len(linew) > 1 and linew[1] == "Excit":
                        eject.append(linew[2])

                """Manage multiple detects in one sequence"""
                if self.filename.find('A0') > 0 and len(self.detectBuffer) > 0:
                    self.detection = self.detectBuffer[0]
                    self.excitation = excit[0]
                if self.filename.find('B0') > 0 and len(self.detectBuffer) > 1:
                    self.detection = self.detectBuffer[1]
                    self.excitation = excit[1]
                if self.filename.find('C0') > 0 and len(self.detectBuffer) > 2:
                    self.detection = self.detectBuffer[2]
                    self.excitation = excit[2]
                if self.filename.find('D0') > 0 and len(self.detectBuffer) > 3:
                    self.detection = self.detectBuffer[3]
                    self.excitation = excit[3]
                if self.filename.find('E0') > 0 and len(self.detectBuffer) > 4:
                    self.detection = self.detectBuffer[4]
                    self.excitation = excit[4]
                if self.filename.find('F0') > 0 and len(self.detectBuffer) > 5:
                    self.detection = self.detectBuffer[5]
                    self.excitation = excit[5]
                if self.filename.find('G0') > 0 and len(self.detectBuffer) > 6:
                    self.detection = self.detectBuffer[6]
                    self.excitation = excit[6]
                if self.filename.find('H0') > 0 and len(self.detectBuffer) > 7:
                    self.detection = self.detectBuffer[7]
                    self.excitation = excit[7]
                if self.filename.find('I0') > 0 and len(self.detectBuffer) > 8:
                    self.detection = self.detectBuffer[8]
                    self.excitation = excit[8]
                if self.filename.find('J0') > 0 and len(self.detectBuffer) > 9:
                    self.detection = self.detectBuffer[9]
                    self.excitation = excit[9]

                for buf in buffers:
                    if buf[1] == self.excitation:
                        self.excitBuffer.append(buf)

                for ejection in eject:
                    for buf in buffers:
                        if buf[1] == ejection:
                            self.ejection.append(ejection)
                            self.ejectBuffer.append(buf)

                for excit in excitbuf:
                    if excit[1] == self.excitation:
                        if len(excit) > 2:
                            self.excitDuration = float(excit[3]) / 1000.0
                        else:
                            self.excitDuration = 0.0

                log.debug("excit duration (s) = %s", self.excitDuration)
                log.debug("all ejections = %s", self.ejectBuffer)
                log.debug("ejections used = %s", self.ejection)
                log.debug("all excitations = %s", self.excitBuffer)
                log.debug("excitation used = %s", self.excitation)
                log.debug("all detections = %s", self.detectBuffer)
                log.debug("detection used = %s", self.detection)
        else:
            print("Filename does not exist:", self.filename + "_sc.txt")

    def get_excit(self):
        return self.excitBuffer, self.excitation

    def get_excit_duration(self):
        return self.excitDuration

    def get_eject(self):
        return self.ejectBuffer, self.ejection

    def get_detect(self):
        return self.detectBuffer, self.detection


if __name__ == '__main__':

    from pkg.dataset import RawDataset

#     filename = "G:\\DATA_PIRENEA_OLD\\DATA_2014\\data140730\\30_07_2014_001.B00"
    # NO SCRIPT !!
    filename = "G:\\PIRENEA_manips\\2006\\data_2006_06_07\\2006_06_07_002.A00"
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_05_12\\2014_05_12_001.B00"
    filename = "G:\\PIRENEA_manips\\2014\\data_2014_07_30\\2014_07_30_001.A00"
#     filename = "D:\\PIRENEA_manips\\data140515\\15_05_2014_001.A00"
#     filename = "G:\\DATA_PIRENEA_OLD\\DATA_2014\\data140515\\15_05_2014_001.A00"
    d = RawDataset(filename)
    data, step = d.get_science()
    print("Number of points: ", len(data))
    print("Step time: ", step)

    s = Script(filename)
    excitBuffer, excitation = s.get_excit()
    ejectBuffer, ejection = s.get_eject()
    detectBuffer, detection = s.get_detect()
    print("ejection", ejection)
    print("detection", detection)
    for eject in ejectBuffer:
        text = ""
        for i, element in enumerate(eject):
            if i > 0:
                text = text + element + " "
        print("text = ", text)
        print("format", "{:.1f}".format(float(eject[3])))
else:
    print("\nImporting... ", __name__)
