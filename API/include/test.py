#!/usr/local/bin/python3
import time

from irc import IRC

host = "irc.rizon.net"
port = 6667
tls = False
nick = "TEST"
pwd = None
chan = "#pwnyan"
debug = True

irc = IRC(host, port)
print("irc.conn()")
irc.conn()
irc.join()



