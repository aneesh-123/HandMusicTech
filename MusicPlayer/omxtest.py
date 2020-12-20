from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import evdev,time,glob
import pygame

# pip3 install omxplayer-wrapper

def playerExit(code):
    print('exit',code)
    global playing
    playing=False

def playFile(file, volume):
    global player,playing
    if player==None:
        player=OMXPlayer(file)
        player.set_volume(volume)
        player.exitEvent += lambda _, exit_code: playerExit(exit_code)
    else:
        player.load(file)
    print('Playing:',file)
    playing=True

def quitPlayer():
    if player!=None:
        player.quit()

def getDevice():
    for fn in evdev.list_devices():
        device = evdev.InputDevice(fn)
        caps = device.capabilities()
        if evdev.events.EV_KEY in caps:
            if evdev.ecodes.KEY_1 in caps[evdev.events.EV_KEY]:
                return device

    raise IOError('No keyboard found')



pygame.init()
win = pygame.display.set_mode((100,100))

player = None
volume = 1.0
VIDEO_PATH = '/home/pi/Music/213.mp3'

import click

playFile(VIDEO_PATH, volume)
i = 0
while i < 50:
    sleep(1)
#     if click.confirm('increase volume'):
#         volume += 0.1
#         player.set_volume(volume)
    change_volume = click.prompt('volume?')
    if change_volume == '+':
        volume += 1
        player.set_volume(volume)
    elif change_volume == '-':
        volume -= 1
        player.set_volume(volume)
    elif change_volume == 'q':
        quitPlayer()
        break;
    else:
        pass
    i += 1
    
quitPlayer()

# while True:
#     for eve in pygame.event.get():pass
#     keyInput = pygame.key.get_pressed()
#     playFile(VIDEO_PATH)
#     if keyInput [pygame.K_a]:
#           quitPlayer()
# 
# 