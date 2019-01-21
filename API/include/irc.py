#!/usr/local/bin/python2.7
import socket
import sys
import ssl
import time
import select

from include import log
logger = log.logger

def write_log(data):
    d = ''
    for l in data:
        d += l + '\n'
    f = open("log.json", "w")
    f.write(d)
    f.close()

class IRC:
    def __init__(self, host, port, use_tls=False, nick="BRIDGE", verbose=2):
        self.host = host
        self.port = port
        self.tls = use_tls
        self.nick = nick
        self.verbose = verbose

        self.running = False
        self.chan = "#DSOB_CHAN"
        self.sock = None
        self.msg_log = []

    # Function to open socket
    def open_sock(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Fucntion to close socket
    def close_sock(self):
        if (self.sock):
            self.sock.close()
        else:
            return

    # Function to connect to server
    def conn(self):
        self.open_sock()
        ret = None
        logger.log("Connecting to IRC...", self.verbose)
        try:
            self.sock.connect((self.host, self.port))
            logger.ok(" ** IRC: Connected.", self.verbose)
            rdy = select.select([self.sock], [], [], 15)
            if (rdy[0]):
                rsp = self.sock.recv(1024)
                logger.log(" ** IRC: %s" % rsp, self.verbose)
            else:
                logger.fatal("Timeout from IRC")
                return -1
            
            # If we connected, authenticate
            self.sock.send("PASS none\r\n")
            self.sock.send("NICK %s\r\n" % str(self.nick))
            self.sock.send("USER %s BOT BOT BOT\r\n" % str(self.nick))
            
            while True:
                rdy = select.select([self.sock], [], [], 10)
                if (rdy[0]):
                    data = self.sock.recv(1024)
                    logger.log("** IRC: %s" % str(data), self.verbose)
                    if ("PING" in data):
                        data = data.replace("PING", "PONG")
                        self.sock.send(data)
                        logger.log(" ** IRC Replied to PING", self.verbose)
                else:
                    break
        except Exception as Err:
            logger.fatal(Err)
            return -1
        finally:
            return None

    # Function to get msg log
    def get_log(self):
        ret = ''
        for line in self.msg_log:
            ret += line + '\n'
        return ret

    def die(self):
        self.running = False

    # Join to channel
    # Use thread to call this
    def join_and_log(self):
        self.running = True
        try:
            self.sock.send("\r\nJOIN %s\r\n" % self.chan)
            while self.running:
                r = select.select([self.sock], [], [], 5)
                if (r[0] == None):
                    print("r[0] == None")
                    continue
                else:
                    print("r[0] != None")
                    msg = self.sock.recv(1024)
                if ("PING") in msg:
                    msg = msg.replace("PING", "PONG")
                    self.sock.send(msg)
                else:
                    try:
                        msg = msg.replace("\n", "")
                        msg = msg.replace("\r", "")
                        msg = msg.replace('"', '\\"')

                        nick = msg.split("!")[0]
                        nick = nick.replace(":", "")
                        data = msg.split(self.chan)[1]
                        data = data.split(":")[1]
                
                        #data = '{"%s", "%s"}' % (nick, data)
                        data2 = '{"Nick": "%s", ' % (nick)
                        data2 += '"Message": "%s"}' % (data)

                        data = data2

                        if ("BRIDGE" in data):
                            continue

                        if (len(self.msg_log) < 80):
                            self.msg_log.append(data)
                        else:
                            for i in range(len(self.msg_log)-1):
                                self.msg_log[i] = self.msg_log[i+1]
                            self.msg_log[i+1] = data
                        write_log(self.msg_log)
                    except Exception as Err:
                        logger.log("Invalid msg", self.verbose)
                        print(Err)

        except Exception as Err:
            print(Err)


