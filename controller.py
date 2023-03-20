"""
controller.py -- Sean Sweeney
Controler class exectutes event based changes on interfaces and songs
"""

import pygame as pg
from song import *
from interface import Interface
from time import time
from events import *
import tkinter as tk
from tkinter import filedialog

verb:bool = True

class Controller(object):

    def __init__(self, song, gui):
        self.song = song
        self.gui = gui
        self.startTime = 0
        self.noteInterval = 60/self.song.tempo
        self.curNote = 0
        self.running = True
    
    def run(self):
        pg.mixer.init()
        root = tk.Tk()
        root.withdraw()

        #init test song
        kick = Sound("kick", "kick.wav")
        snare = Sound("snare", "snare.wav")
        self.song.curSection.addChannel(self.song.nnotes, kick)
        self.song.curSection.addChannel(self.song.nnotes, snare)

        self.gui.start(self.song.nnotes)
        curNote = 0
        nextTimeToPlay = time() + 1
        while self.running:
            self.executeEvent(self.gui.checkEvents())
            self.gui.backgroundFill()
            self.gui.drawSong(self.song)
            self.gui.update()
            if self.song.play and time() >= nextTimeToPlay:
                if verb: print(f"triggered play note at index {curNote}")
                self.song.playNote(curNote)
                nextTimeToPlay += self.noteInterval
                curNote += 1
                if curNote >= self.song.nnotes:
                    curNote = 0
        self.gui.quit()

    def executeEvent(self, e:Event):
        if verb:
            if e != None: print(f"cont.executeEvent input: {e}")
        match e:
            case QuitEvent():
                self.running = False
            case ClickNoteEvent(chani,notei):
                if verb: print("click note event")
                if verb: print(f"before toggle play={self.song.curSection.channels[chani].played[notei]}")
                self.song.curSection.channels[chani].toggleNote(notei)
                if verb: print(f"after toggle play={self.song.curSection.channels[chani].played[notei]}")
            case ClickPlayEvent():
                self.song.play = True
                self.gui.play = True
                self.startTime = time()
            case ClickPauseEvent():
                self.song.play = False
                self.gui.play = False
                self.curNote = 0
            case None:
                pass
            case _:
                self.running = False
                print(f"encountered unexpected event in controller.executeEvent(): {e}")
            
