"""
main.py -- Sean Sweeney
main method for sequencer prototype
"""

import pygame as pg
from song import *
from interface import Interface
from time import time

verb = True

def main():
    song:Song = Song("test")
    gui:Interface = Interface()
    gui.start()
    running:bool = True
    curNote = 0
    nextTimeToPlay = time() + 1
    while running:
        running = gui.checkEvents(song)
        gui.backgroundFill()
        gui.drawTools()
        gui.drawSong(song)
        gui.update()
        if song.play and time() >= nextTimeToPlay:
            if verb: print(f"triggered play note at index {curNote}")
            song.playNote(curNote)
            nextTimeToPlay += 60/song.tempo
            curNote += 1
            if curNote >= song.nbars*song.nbeats:
                curNote = 0
    gui.quit()


if __name__ == "__main__":
    main()