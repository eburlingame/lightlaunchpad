__author__ = 'eric'

from launchpad.launchpad import *
from pygame import time
from command import *
from client import *
import os
import re

class Main:
    def __init__(self):
        if len(sys.argv) < 2:
            print "Not enough arguments"
            quit()

        address = sys.argv[1]

        wd = os.path.dirname(os.path.realpath(__file__))
        path = wd + "/config.txt"
        self.server = ServerClient(address, self)
        self.commands = self.parse_config(path)

        self.LP = Launchpad()  # creates a Launchpad instance (first Launchpad found)
        self.LP.Open()  # start it
        self.LP.Reset()
        self.run_launchpad()

    def parse_config(self, filepath):
        file = open(filepath, "r")

        commands = []
        current = ""
        for line in file:
            if re.match("Button(.+)", line):
                if current != "":
                    commands.append(TriggerCommand(current, self.server))
                    current = line
                else:
                    current += line
            else:
                current += line
        if current != "":
            commands.append(TriggerCommand(current, self.server))

        return commands

    def print_commands(self):
        for command in self.commands:
            command.to_string()

    def find_trigger(self, x, y):
        for command in self.commands:
            if command.button[0] == x and command.button[1] == y:
                return command
        return False

    def button_press(self, x, y, state):
        # print "Pressed %s at %s, %s" % (state, x, y)
        cmd = self.find_trigger(x, y)
        if cmd == False:
            # print "Could not find command"
            return

        if state:
            cmd.press_down()
        else:
            cmd.press_up()

        self.update_leds()

    def reset_added(self):
        for command in self.commands:
            command.added = False

    def color_test(self):
        for x in range(0, 4):
            for y in range(0, 4):
                self.LP.LedCtrlXY(x, y+1, x, y)

    def update_leds(self):
        for command in self.commands:
            self.LP.LedCtrlXY(command.x, command.y, command.get_color()[0], command.get_color()[1])

    def run_launchpad(self):
        self.update_leds()
        while 1:
            # some extra time to give the button events a chance to come through...
            time.wait(5)

            if self.LP.ButtonChanged():
                x, y, state = self.LP.ButtonStateXY()
                self.button_press(x, y, state)


        self.LP.Reset()  # turn all LEDs off
        self.LP.Close()  # close the Launchpad

if __name__ == '__main__':
    main = Main()
