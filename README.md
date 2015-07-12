# Light Launch Pad

This is a simple Python program that interfaces with a 
[Novation Launchpad Mini](http://global.novationmusic.com/launch/launchpad-mini#) via the [launchpad.py library by 
FMMT666](https://github.com/FMMT666/launchpad.py), and send preconfigured commands to a 
[DMXLightingServer](https://github.com/eburlingame/lightingserver). Though the program can be used tosend commands via
a websocket to any kind of server.

The script reads a simple text configuration file which identifies which commands to run, which are then sent
 to the server when the button on the LaunchPad is pressed.
 
## Linux Install

- Clone the repository: `git clone https://github.com/eburlingame/lightlaunchpad.git`
- Enter the folder: `cd lightlaunchpad`
- Install websocket-client: `sudo pip install websocket-client`
- Clone [launchpad.py](https://github.com/FMMT666/launchpad.py.git)
    - `git clone https://github.com/FMMT666/launchpad.py.git`
- Make an `__init__.py` so it can be imported
    - Rename `launchpad.py` to `launchpad`: `mv launchpad.py/ launchpad`
    - Enter the folder: `cd launchpad`
    - Create the file: `vim __init__.py`
    - Quit vim: Hit escape, then enter `:wq`

## Run At Login

Edit `/etc/profile`:

`vim /etc/profile`

Add at the bottom:

`python lightlaunchpad/main.py ws://localhost:8080/ws &`

Adding `&` at the end will start the process in the background.