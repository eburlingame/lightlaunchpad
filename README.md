# Light Launch Pad

This is a simple Python program that interfaces with a 
[Novation Launchpad Mini](http://global.novationmusic.com/launch/launchpad-mini#) via the [launchpad.py library by 
FMMT666](https://github.com/FMMT666/launchpad.py), and send preconfigured commands to a 
[DMXLightingServer](https://github.com/eburlingame/lightingserver). Though the program can be used tosend commands via
a websocket to any kind of server.

The script reads a simple text configuration file which identifies which commands to run, which are then sent
 to the server when the button on the LaunchPad is pressed.