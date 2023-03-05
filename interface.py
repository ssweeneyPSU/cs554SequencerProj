"""
interface.py -- Sean Sweeney
class to draw sequencer to screen
"""
import pygame as pg
from song import Song

verb = False #verbose tag for printing

MARGIN = 2
TOOLMARGIN = 3
TOOLBARFRAC = 1/6
CHANNELTITLEFRAC = 1/10

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
        self.toolbar_h = TOOLBARFRAC*self.height
        self.toolbar_w = self.width
        self.tool_y = MARGIN+TOOLMARGIN
        self.tool_h = self.toolbarHeight-2*TOOLMARGIN
        self.seq_y = self.toolbarHeight+MARGIN
        self.channel_h = 0
        self.channeltitle_w = CHANNELTITLEFRAC*(self.w-2*MARGIN)
        self.channel_x = self.channeltitle_w+2*MARGIN
        self.note_w = 0

    def start(self, init_nnotes):
        pg.init()
        self.screen = pg.display.set_mode([self.w, self.h])
        self.set_nnotes(init_nnotes)
    
    def update(self):
        pg.display.flip()

    def quit(self):
        pg.quit()

    def set_nnotes(self, new_nnotes):
        self.nnnotes = new_nnotes
        self.note_w = (self.w - (self.channeltitle_w+2*MARGIN) - MARGIN)//self.nnotes
    
    def set_nnchannels(self, new_nnchannels):
        self.nchannels = new_nnchannels
        self.channel_h = (self.h - self.toolbar_h)//8 if self.nchannels <= 8 else (self.h - self.toolbar_h)//self.nchannels

    def backgroundFill(self, color=BLACK):
        self.screen.fill(color)
    
    def initToolbar(self):
        self.buttons += [Button(MARGIN+TOOLMARGIN,self.tool_y, self.tool_h,self.tool_h, PAUSERED, "PLAY")]
        self.buttons += [Button(MARGIN+2*TOOLMARGIN+self.tool_h, self.tool_y, 2*self.tool_h, self.tool_h, TOOLGREY, "ADD")]

    def drawToolbar(self):
        if self.nbuttons == 0: self.initToolbar()
        pg.draw.rect(self.screen, WHITE, [MARGIN, self.toolbar_y, self.toolbar_w, self.toolbar_h])
        for button in self.buttons:
            button.draw(self.screen)

    def initSequencer(self):
        self.notes = []
        for channel_i in range(self.nchannels):
            curchannel_y = self.seq_y+(self.channel_h+MARGIN)*channel_i
            for note_i in range(1,self.nnotes+1):
                curnote_x = self.channel_x+(self.note_w+MARGIN)*note_i
                self.notes += [Note(curnote_x, curchannel_y, self.note_w, self.channel_h)]

    def drawSequncer(self,song):
        if self.nchannels == 0:
            return
        #note_w = (self.w - (self.channeltitle_w+2*MARGIN) - MARGIN)//song.nnotes
        for channel_i in range(self.nchannels):
            curchannel_y = self.seq_y+(self.channel_h+MARGIN)*channel_i
            pg.draw.rect(self.screen, WHITE, [MARGIN, curchannel_y, self.channeltitle_w, self.channel_h])
        for note in self.notes: 
            note.draw(self.screen)
            

    def drawChannel(self, channel_y, nnotes, played_arr):
        for note_i in range(1,nnotes+1):
                curnote_x = self.channel_x+(self.note_w+MARGIN)
                color = YELLOW if played_arr[note_i-1] else WHITE
                pg.draw.rect(self.screen, color, [curnote_x, channel_y, self.note_w, self.channel_h]) 

    def drawSong(self, song:Song):
        self.drawToolbar()
        self.drawSequncer(song)



class Button(pg.rect):

    def __init__(self, x, y, w, h, text, color):
        self.left = x
        self.top = y
        self.width = w
        self.height = h
        self.text = text
        self.color = color
        self.font = None

    def draw(self, screen):
        if not self.font: 
            self.font = pg.font.Font('ariel', self.h-TOOLMARGIN)
        name = self.font.render(self.text, False, BLACK, self.color)
        screen.blit(name, self)

    def is_clicked(self, mx, my):
        return mx >= self.top and mx <= self.top+self.width and my >= self.left and my <= self.left+self.height
    
class Note(pg.rect):
    
    def __init__(self, x, y, w, h, play):
        self.left = x
        self.top = y
        self.width = w
        self.height = h
        self.play = play

    def draw(self, screen):
        color = YELLOW if self.play else WHITE
        pg.draw.rect(screen, color, [self.left, self.top, self.width, self.height]) 
    
    def is_clicked(self, mx, my):
        return mx >= self.top and mx <= self.top+self.width and my >= self.left and my <= self.left+self.height
    