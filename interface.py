"""
interface.py -- Sean Sweeney
class to draw sequencer to screen
"""
import pygame as pg
from song import Song

BLACK = (255,255,255)

class Interface(object):

    def __init__(self):
        self.height:int = 500 #total window height
        self.width:int  = 500 #total window width

    def drawSong(self, screen, song:Song):
        screen.fill(BLACK)


    