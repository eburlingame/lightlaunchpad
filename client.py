__author__ = 'eric'
import sys
from websocket import create_connection
import re

class ServerClient:

    def __init__(self, address, main):
        self.current_command = ""
        self.main = main
        self.addr = address
        self.connect()

    def connect(self):
        try:
            self.ws = create_connection(self.addr)
            print "Connected to %s" % self.addr
        except:
            print "Could not connect to %s" % self.addr

    # Adds to the current command buffer
    def add_to_command(self, command):
        self.current_command += command + " "
        print "Command Buffer: %s" % self.current_command

    # Runs a command by itself
    def run_command(self, command):
        if command != "":
            self.send_command(command)

    # Runs the command saved in the buffer
    def execute_command(self):
        if self.current_command != "":
            self.send_command(self.current_command)
            self.current_command = ""
            self.main.reset_added()

    def send_command(self, command):
        try:
            print "Calling '%s'" % command
            self.ws.send(command)
            result =  self.ws.recv()
            result = re.sub("<br />", "\n", result)
            print result
        except:
            print "Could not connect to server; retrying..."
            self.connect()


    def close(self):
        self.ws.close()