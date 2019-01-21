#!/usr/local/bin/python2.7
"""
This file handles HTTP-interface for irc logger.

Last edit: 16/12/18 (dd/mm/yy) - <k4m1@protonmail.com>

"""
import socket

from include import irc
from include import log

logger = log.logger

class API:
    def __init__(self, host, port, irc_mod, verbose):
        self.host = host
        self.port = port
        self.irc  = irc_mod
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.verbose = verbose

    def get_log(self):
        rsp = "HTTP/1.1 200 Ok\r\n"
        rsp += "Host: wonderland.is.cool\r\n"
        rsp += "Server: None of your business\r\n"
        rsp += "Content-Length: <replace>\r\n"
        rsp += "\r\n"

        msgs = self.irc.get_log()

        rsp = rsp.replace("<replace>", str(len(msgs)))
        rsp += msgs
        rsp += '\r\n\r\n'
        return rsp

    def run(self):
        try:
            self.sock.bind((self.host, self.port))
            logger.ok("Listening to %s:%s\n" % (self.host, self.port),
                    self.verbose)
            while True:
                self.sock.listen(1)
                conn, addr = self.sock.accept()
                logger.log("Connection from %s accepted" % conn, self.verbose)
                conn.send(self.get_log())
                conn.close()
        except Exception as Err:
            logger.fatal(Err)
            return -1





