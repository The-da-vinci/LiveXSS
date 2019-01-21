#!/usr/local/bin/python3
"""
This file provides logging utilities.

Verbosity levels:
    0 = minimal output
    1 = normal output
    2 = debugging output

Last edit: 16/12/18 (dd/mm/yy) - <k4m1@protonmail.com>
"""

class logger:
    @staticmethod
    def fatal(msg):
        print("[fail] %s" % str(msg))

    @staticmethod
    def log(msg, verbose):
        if (verbose == 2):
            print("[info] %s" % str(msg))

    @staticmethod
    def ok(msg, verbose):
        if (verbose >= 1):
            print("[ ok ] %s" % str(msg))
  



