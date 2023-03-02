"""
interface.py -- Sean Sweeney
class to draw sequencer to screen
"""
import pygame as pg
from song import Song
from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN,
)
verb = False #verbose tag for printing

MARGIN = 1
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)


class Interface(object):

    def __init__(self):
        self.height:int = 500 #total window height
        self.width:int  = 700 #total window width

    def start(self):
        pg.init()
        self.screen = pg.display.set_mode([self.width, self.height])
    
    def update(self):
        pg.display.flip()

    def quit(self):
        pg.quit()

    def drawSong(self, song:Song):
        self.screen.fill(BLACK)
        numChan = len(song.curSection.channels)
        numNotes = song.nbars*song.nbeats
        noteSize = (self.width-(numNotes+2)*MARGIN)//(numNotes+1)
        for channelNum in range(numChan):
            pg.draw.rect(self.screen, WHITE, [MARGIN, (noteSize+MARGIN)*channelNum, noteSize, noteSize])
            for n in range(1,numNotes+1):
                color = WHITE
                if song.curSection.channels[channelNum].played[n-1]: color = YELLOW
                pg.draw.rect(self.screen, color, [(MARGIN + noteSize)*n+MARGIN, (noteSize+MARGIN)*channelNum, noteSize, noteSize])

    def checkEvents(self, song) -> bool:
        for event in pg.event.get():
            if event.type == QUIT:
                return False
            if event.type == MOUSEBUTTONDOWN:
                
                mx, my = pg.mouse.get_pos()
                print(f"mouse click at {mx}, {my}")
                self.clickNote(song, mx, my)
        return True

    def clickNote(self, song, mousex, mousey):
        numChan = len(song.curSection.channels)
        numNotes = song.nbars*song.nbeats
        noteSize = (self.width-(numNotes+2)*MARGIN)//(numNotes+1)
        chanClicked = mousey // (noteSize+MARGIN)
        if verb: print(f"chan index clicked: {chanClicked}")
        if chanClicked > numChan-1: return
        noteClicked = (mousex-(noteSize+MARGIN)) // (noteSize+MARGIN)
        if verb: print(f"note index clicked: {noteClicked}")
        if noteClicked < 0 or noteClicked > numNotes-1: return
        song.curSection.channels[chanClicked].played[noteClicked] = not  song.curSection.channels[chanClicked].played[noteClicked] 



    