"""
events.py -- Sean Sweeney
the EventHandler class is created and called every loop so that the logic for drawing and handling interaction are separated out. 
"""
import pygame as pg
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN,
)

verb = False

class EventHandler(object):

    def __init__(self, buttons, notes):
        self.buttons = buttons
        self.notes = notes

    def checkEvents(self, song) -> bool:
        for event in pg.event.get():
            if event.type == QUIT:
                return False
            if event.type == MOUSEBUTTONDOWN:
                self.executeMouseEvent(song)
        return True
    
    def executeMouseEvent(self, song):
        mx, my = pg.mouse.get_pos()
        if verb: print(f"mouse click at {mx}, {my}")
        self.clickNote(song, mx, my)

    def clickNote(self, song, mousex, mousey) -> bool:
        numChan = len(song.curSection.channels)
        numNotes = song.nbars*song.nbeats
        noteSize = (self.width-(numNotes+2)*MARGIN)//(numNotes+1)
        chanClicked = (mousey-(self.toolbarHeight+2*MARGIN)) // (noteSize+MARGIN)
        noteClicked = (mousex-(noteSize+MARGIN)) // (noteSize+MARGIN)
        if verb: print(f"chan index clicked: {chanClicked}, note index clicked: {noteClicked}")
        if chanClicked < 0 or chanClicked > numChan-1 or noteClicked < 0 or noteClicked > numNotes-1: 
            return False
        song.curSection.channels[chanClicked].played[noteClicked] = not  song.curSection.channels[chanClicked].played[noteClicked] 
        return True