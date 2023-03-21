"""
interface.py -- Sean Sweeney
class to draw sequencer to screen
"""
import pygame as pg
from song import Song
from events import *

from pygame.locals import (
    QUIT,
    MOUSEBUTTONDOWN,
)


verb = True #verbose tag for printing

MARGIN = 2
TOOLMARGIN = 3
TOOLBARFRAC = 1/7
CHANNELTITLEFRAC = 1/11
TEXTFRAC = 1/2

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
PLAYGREEN = (89, 179, 54)
PAUSERED = (186, 11, 34)
TOOLGREY = (125,125,125)


class Interface(object):

    def __init__(self):
        self.h:int = 600 #total window height
        self.w:int  = 1200 #total window width
        self.buttons = []
        self.nbuttons = 0
        self.notes = []
        self.play = False
        self.nchannels = 0
        self.nnotes = 0
        self.toolbar_y = MARGIN #toolbar y position
        self.toolbar_h = int(TOOLBARFRAC*self.h)
        self.toolbar_w = self.w
        self.tool_y = MARGIN+TOOLMARGIN
        self.tool_h = self.toolbar_h-2*TOOLMARGIN
        self.seq_y = self.toolbar_h+MARGIN
        self.channel_h = 0
        self.channeltitle_w = int(CHANNELTITLEFRAC*(self.w-2*MARGIN))
        self.channel_x = self.channeltitle_w+2*MARGIN
        self.note_w = 0

    def start(self, init_nnotes):
        pg.init()
        self.screen = pg.display.set_mode([self.w, self.h])
        self.set_nnotes(init_nnotes)
        self.set_nchannels(2)
    
    def update(self):
        pg.display.flip()

    def quit(self):
        pg.quit()

    def set_nnotes(self, new_nnotes):
        self.nnotes = new_nnotes
        self.note_w = (self.w - (self.channeltitle_w+2*MARGIN) - self.nnotes*MARGIN)//self.nnotes
    
    def set_nchannels(self, new_nnchannels):
        self.nchannels = new_nnchannels
        self.channel_h = (self.h - self.toolbar_h)//8 if self.nchannels <= 8 else (self.h - self.toolbar_h)//self.nchannels

    def backgroundFill(self, color=BLACK):
        self.screen.fill(color)
    
    def initToolbar(self):
        self.buttons += [Button(MARGIN+TOOLMARGIN,self.tool_y, self.tool_h,self.tool_h, "", PLAYGREEN, "play")]
        self.buttons += [Button(MARGIN+2*TOOLMARGIN+self.tool_h, self.tool_y, 2*self.tool_h, self.tool_h, "ADD", TOOLGREY, "add channel")]
        self.buttons += [Button(MARGIN+3*TOOLMARGIN+3*self.tool_h, self.tool_y, self.tool_h//2, self.tool_h, "<", TOOLGREY, "lower tempo")]
        self.buttons += [Button(MARGIN+4*TOOLMARGIN+3*self.tool_h+self.tool_h//2, self.tool_y, self.tool_h, self.tool_h, "Tempo", TOOLGREY, "tempo")]
        self.buttons += [Button(MARGIN+5*TOOLMARGIN+5*self.tool_h, self.tool_y, self.tool_h//2, self.tool_h, ">", TOOLGREY, "raise tempo")]
        self.buttons += [Button(MARGIN+6*TOOLMARGIN+5*self.tool_h+self.tool_h//2, self.tool_y, self.tool_h+self.tool_h//2, self.tool_h, "Save", TOOLGREY, "save")]
        self.buttons += [Button(MARGIN+8*TOOLMARGIN+6*self.tool_h+self.tool_h//2, self.tool_y, self.tool_h, self.tool_h, "Load", TOOLGREY, "load")]
        

    def drawToolbar(self):
        if self.nbuttons == 0: self.initToolbar()
        pg.draw.rect(self.screen, WHITE, [MARGIN, self.toolbar_y, self.toolbar_w, self.toolbar_h])
        for button in self.buttons:
            button.draw(self.screen)
        
    def drawSequncer(self,song):
        for channel_i in range(song.curSection.nchannels):
            curchannel_y = self.seq_y+MARGIN+(self.channel_h+MARGIN)*channel_i
            pg.draw.rect(self.screen, WHITE, [MARGIN, curchannel_y, self.channeltitle_w, self.channel_h])
            self.drawChannel(curchannel_y, song.nnotes, song.curSection.channels[channel_i].played)    

    def drawChannel(self, channel_y, nnotes, played_arr):
        for note_i in range(nnotes):
                curnote_x = self.channel_x+(self.note_w+MARGIN)*note_i
                color = YELLOW if played_arr[note_i] else WHITE
                pg.draw.rect(self.screen, color, [curnote_x, channel_y, self.note_w, self.channel_h]) 

    def drawSong(self, song:Song):
        self.drawToolbar()
        self.drawSequncer(song)

    def checkEvents(self) -> Event:
        for event in pg.event.get():
            if event.type == QUIT:
                return QuitEvent()
            if event.type == MOUSEBUTTONDOWN:
                return self.executeMouseEvent()
        return None
    
    def executeMouseEvent(self):
        mx, my = pg.mouse.get_pos()
        if verb: print(f"execute mouse click at {mx}, {my}")
        if my < self.toolbar_h:
            if verb: print(f"going to click button")
            return self.clickButton(mx, my)
        return self.clickNote(mx, my)

    def clickNote(self, mousex, mousey) -> str:
        chanClicked = (mousey-(self.toolbar_h+2*MARGIN)) // (self.channel_h+MARGIN)
        noteClicked = (mousex-(self.channeltitle_w+2*MARGIN)) // (self.note_w+MARGIN)
        if verb: print(f"chan index clicked: {chanClicked}, note index clicked: {noteClicked}")
        if chanClicked < 0 or chanClicked > self.nchannels-1 or noteClicked < 0 or noteClicked > self.nnotes-1: 
            return None
        if verb: print(f"clicked chan {chanClicked}, note {noteClicked}")
        return ClickNoteEvent(chanClicked,noteClicked)

    def clickButton(self, mx, my) -> Event:
        if verb: print(f"top of click button at {mx}, {my}")
        for button in self.buttons:
            if verb: print(f"in clickButton, button to check: {button.name}")
            if button.is_clicked(mx, my):
                if verb: print("button was clicked")
                match button.name:
                    case "play":
                        if button.color == PLAYGREEN:
                            button.changeColor(PAUSERED)
                            button.draw(self.screen)
                            if verb: print("returning a click play event")
                            return ClickPlayEvent()
                        elif button.color == PAUSERED:
                            button.changeColor(PLAYGREEN)
                            button.draw(self.screen)
                            if verb: print("returning a clickPauseEvent")
                            return ClickPauseEvent()
                    case "add channel":
                        if verb: print("returning an AddChannelEvent")
                        return AddChannelEvent()
                    case "lower tempo":
                        return LowerTempoEvent()
                    case "tempo":
                        return None
                    case "raise tempo":
                        return RaiseTempoEvent()
                    case "save":
                        return SaveEvent()
                    case "load":
                        return LoadEvent()
                    case _:
                        print(f"caught unexpected button in gui.clickButton: {button.name}")

    
class Button(object):

    def __init__(self, x, y, w, h, text, color, name):
        self.left = x
        self.top = y
        self.width = w
        self.height = h
        self.text = text
        self.color = color
        self.font = None
        self.name = name

    def changeColor(self, newColor):
        self.color = newColor

    def draw(self, screen):
        if not self.font: 
            self.font = pg.font.SysFont('Arial', int(self.height*TEXTFRAC))
        name = self.font.render(self.text, False, BLACK)
        pg.draw.rect(screen, self.color, [self.left, self.top, self.width, self.height])
        screen.blit(name, (self.left, self.top))

    def is_clicked(self, mx, my):
        return mx >= self.left and mx <= self.left+self.width and my >= self.top and my <= self.top+self.height
