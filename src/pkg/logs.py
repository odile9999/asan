#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#        Copyright (c) IRAP CNRS
#        Odile Coeur-Joly, Toulouse, France
#
"""
Define a global logger for the project.
Picked up from http://stackoverflow.com/questions/7621897/python-logging-module-globally

pkg.log Created on 9 oct. 2015
"""
import logging
log = logging.getLogger('root')


class Logs(object):
    """
    Define a global logger.
    """

    def __init__(self, name):
        """
        Constructor
        """
        self.name = name

    def setup_logger(self, level):

        logger = logging.getLogger(self.name)
        if level == "debug":
            logger.setLevel(logging.DEBUG)
        if level == "info":
            logger.setLevel(logging.INFO)
        if level == "error":
            logger.setLevel(logging.ERROR)
        # complete format with date
#         formatter = logging.Formatter(
#             "%(asctime)s - %(levelname)s - %(module)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        # simple format without date
        formatter = logging.Formatter(
            "%(levelname)s :: %(module)s/%(funcName)s :: %(message)s")

        handler = logging.StreamHandler()
#         handler = logging.FileHandler("toto.log")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

if __name__ == '__main__':
    pass
else:
    log.info("Importing... %s", __name__)
