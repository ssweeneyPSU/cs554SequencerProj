"""
main.py -- Sean Sweeney
main method for sequencer prototype
"""

import pygame as pg
from song import *
from interface import Interface
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

def main():
    song:Song = Song("test")
    gui:Interface = Interface()
    screen = pg.display.set_mode([gui.height, gui.width])
    running:bool = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
        screen.fill((0,0,0))
        pg.display.flip()
    pg.quit()



if __name__ == "__main__":
    main()