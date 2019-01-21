#!/usr/local/bin/python2.7
"""
This file handles controlling both IRC bridge, as well as
serving the web API for any crappy code that might want to
look at IRC log for reason or another :)

IRC Log is returned in following JSON format:

    {"Nick": "<nick>", "Message": "<message>"}
    {"Nick": "<other>", "Message": "<new one>"}
    ...


"""
from threading import Thread

from include import irc
from include import api
from include import log

import time


def main():
    irc_mod = irc.IRC("irc.rizon.net", 6667, False, "DSOB_BRIDGE", 2)
    irc_mod.conn()
    print("\n\n*** Connected, press enter to quit")
    Thread(target=irc_mod.join_and_log).start()
    raw_input()
    irc_mod.die()

if __name__ == "__main__":
    main()

