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
import pickle

verb:bool = True

class Controller(object):

    def __init__(self, song, gui):
        self.song = song
        self.gui = gui
        self.startTime = 0
        self.noteInterval = 60/self.song.tempo
        self.curNote = 0
        self.running = True
        self.nextTimeToPlay = 0
    
    def run(self):
        pg.mixer.init()
        #init test song
        """
        kick = Sound("kick", "kick.wav")
        snare = Sound("snare", "snare.wav")
        self.song.curSection.addChannel(self.song.nnotes, kick)
        self.song.curSection.addChannel(self.song.nnotes, snare)
        """

        self.gui.start(self.song.nnotes)
        curNote = 0
        while self.running:
            self.executeEvent(self.gui.checkEvents())
            self.gui.backgroundFill()
            self.gui.drawSong(self.song)
            self.gui.update()
            if self.song.play and time() >= self.nextTimeToPlay:
                if verb: print(f"triggered play note at index {curNote}")
                self.song.playNote(curNote)
                self.nextTimeToPlay += self.noteInterval
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
                self.song.curSection.channels[chani].toggleNote(notei)
            case ClickPlayEvent():
                if verb: print("click play event")
                self.song.play = True
                self.gui.play = True
                self.startTime = time()
                self.nextTimeToPlay = self.startTime + self.noteInterval
            case ClickPauseEvent():
                if verb: print("click pause event")
                self.song.play = False
                self.gui.play = False
                self.curNote = 0
                self.nextTimeToPlay = 0
            case AddChannelEvent():
                if verb: print("caught add channel")
                top = tk.Tk()
                top.withdraw()
                soundPath = filedialog.askopenfilename(parent=top)
                top.destroy()
                soundName = soundPath.split('\\')[-1].split('.')[0]
                newSound = Sound(soundName, soundPath)
                self.song.curSection.addChannel(self.song.nnotes, newSound, soundName)
                self.gui.set_nchannels(self.song.curSection.nchannels)
            case LowerTempoEvent():
                self.song.tempo -= 1
                self.noteInterval = 60/self.song.tempo
            case RaiseTempoEvent():
                self.song.tempo += 1
                self.noteInterval = 60/self.song.tempo
            case SaveEvent():
                top = tk.Tk()
                top.withdraw()
                filePath = filedialog.asksaveasfilename(parent=top)
                top.destroy()
                with open(filePath, 'wb') as saveFile:
                    pickle.dump(self.song, saveFile)
            case LoadEvent():
                self.executeEvent(ClickPauseEvent())
                top = tk.Tk()
                top.withdraw()
                loadPath = filedialog.askopenfilename(parent=top)
                top.destroy()
                with open(loadPath, 'rb') as loadFile:
                    newSong = pickle.load(loadFile)
                    self.song = newSong
                    self.gui.set_nnotes(newSong.nnotes)
                    self.gui.set_nchannels(newSong.curSection.nchannels)
            case None:
                pass
            case _:
                self.running = False
                print(f"encountered unexpected event in controller.executeEvent(): {e}")
            
