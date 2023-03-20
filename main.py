"""
main.py -- Sean Sweeney
main method for sequencer prototype
"""

from controller import Controller
from song import *
from interface import Interface

verb = True

def main():
    gui:Interface = Interface()
    song:Song = Song("test")
    controller:Controller = Controller(song, gui)
    controller.run()


if __name__ == "__main__":
    main()