__author__ = 'eric'

import re
class Colors:
    UNPRESSED_RUN = (2, 1)
    UNPRESSED_ADD = (2, 0)
    PRESSED_SWITCH = (3, 0)
    PRESSED_BUMP = (0, 3)

class TriggerCommand:

    # Command Config Format:

    # Button (1, 0)
    #     Down: load scene test
    #     Up: load scene test %0
    #     Type: bump //bump or switch
    #     RunOnPress: True

    def __init__(self, raw, server):
        self.server = server
        self.raw = raw
        self.button = self.parse_button()
        self.x = self.button[0]
        self.y = self.button[1]
        self.up = self.parse_up()
        self.down = self.parse_down()
        self.type = self.parse_type()
        self.runOnPress = self.parse_runonpress()

        self.pressed = False

    def parse_button(self):
        patrn = "Button \((\d+), (\d+)\)"
        group = self.parse_or_raise(patrn)
        return (int(group[0][0]), int(group[0][1]))

    def parse_up(self):
        group = self.parse_or_raise("Up:(.+)?")
        return group[0].lower()

    def parse_down(self):
        group = self.parse_or_raise("Down:(.+)?")
        return group[0].lower()

    def parse_type(self):
        group = self.parse_or_raise("Type:\s+?(.+)")
        return group[0].lower()

    def parse_runonpress(self):
        patrn = "RunOnPress:\s+?(.+)"
        group = self.parse_or_raise(patrn)
        return (group[0] == "true" or group[0] == "True")

    def parse_or_raise(self, pattern):
        match = re.findall(pattern, self.raw)
        if len(match) > 0:
            return match
        raise Exception("Invalid file format")

    def to_string(self):
        print "Button: %s, %s" % self.button
        print "Up: %s" % self.up
        print "Down: %s" % self.down
        print "Type: %s" % self.type
        print "RunOnPress: %s" % self.runOnPress

    def press_down(self):
        if self.type == "switch":
            if self.pressed:
                self.run(self.up)
                self.pressed = False
            else:
                self.pressed = True
                self.run(self.down)
        elif self.type == "bump":
            self.pressed = True
            self.run(self.down)

    def press_up(self):
        if self.type == "bump":
            if self.pressed:
                self.run(self.up)
                self.pressed = False

    def run(self, command):
        if self.runOnPress:
            self.server.run_command(command)
        else:
            self.server.add_to_command(command)

    def get_color(self):
        if self.pressed:
            if self.type == "switch":
                return Colors.PRESSED_SWITCH
            else:
                return Colors.PRESSED_BUMP
        else:
            if self.runOnPress:
                return Colors.UNPRESSED_RUN
            else:
                return Colors.UNPRESSED_ADD
