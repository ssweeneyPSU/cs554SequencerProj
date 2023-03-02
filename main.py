"""
main.py -- Sean Sweeney
main method for sequencer prototype
"""

import pygame as pg
from song import *
from interface import Interface


def main():
    song:Song = Song("test")
    gui:Interface = Interface()
    gui.start()
    running:bool = True
    while running:
        running = gui.checkEvents(song)
        gui.drawSong(song)
        gui.update()
    gui.quit()


if __name__ == "__main__":
    main()