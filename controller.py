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

verb:bool = False

class Controller(object):

    def __init__(self, song, gui):
        self.song = song
        self.gui = gui
        self.startTime = 0
        self.noteInterval = 60/self.song.tempo
        self.curNote = -1
        self.running = True
        self.nextTimeToPlay = 0
        self.player = Player()
    
    def run(self):
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()

        self.gui.start(self.song.nnotes)
        while self.running:
            self.executeEvent(self.gui.checkEvents())
            self.gui.backgroundFill()
            self.gui.drawSong(self.song, self.curNote)
            self.gui.update()
            if self.song.play and time() >= self.nextTimeToPlay:
                if verb: print(f"triggered play note at index {self.curNote}")
                self.player.playSounds([i for i in range(self.song.curSection.nchannels) if self.song.curSection.channels[i].played[self.curNote]])    
                self.nextTimeToPlay += self.noteInterval
                self.curNote += 1
                if self.curNote >= self.song.nnotes:
                    self.curNote = 0
            
        self.gui.quit()

    def executeEvent(self, e:Event):
        if verb:
            if e != None: print(f"cont.executeEvent input: {e}")
        match e:
            case QuitEvent():
                self.running = False
            case NoteEvent(chani,notei):
                if verb: print("click note event")
                self.song.curSection.channels[chani].toggleNote(notei)
            case PlayEvent():
                if verb: print("click play event")
                self.song.play = True
                self.gui.play = True
                self.startTime = time()
                self.nextTimeToPlay = self.startTime + self.noteInterval
                self.curNote = 0
            case PauseEvent():
                if verb: print("click pause event")
                self.song.play = False
                self.gui.play = False
                self.curNote = -1
                self.nextTimeToPlay = 0
            case AddChannelEvent():
                if verb: print("caught add channel")
                top = tk.Tk()
                top.withdraw()
                soundPath = filedialog.askopenfilename(parent=top)
                top.destroy()
                soundName = soundPath.split('/')[-1].split('.')[0]
                if verb: print(f"added soundName {soundName} from path {soundPath}")
                #newSound = Sound(soundName, soundPath)
                self.song.curSection.addChannel(self.song.nnotes, soundPath, soundName)
                self.gui.set_nchannels(self.song.curSection.nchannels)
                self.player.addSound(soundPath)
            case LowerTempoEvent():
                self.song.tempo -= 5
                self.noteInterval = 60/self.song.tempo
            case RaiseTempoEvent():
                self.song.tempo += 5
                self.noteInterval = 60/self.song.tempo
            case SaveEvent():
                top = tk.Tk()
                top.withdraw()
                filePath = filedialog.asksaveasfilename(parent=top)
                top.destroy()
                if not filePath: return
                with open(filePath, 'wb') as saveFile:
                    pickle.dump(self.song, saveFile)
            case LoadEvent():
                self.executeEvent(PauseEvent())
                top = tk.Tk()
                top.withdraw()
                loadPath = filedialog.askopenfilename(parent=top)
                top.destroy()
                if not loadPath: return
                with open(loadPath, 'rb') as loadFile:
                    newSong = pickle.load(loadFile)
                    self.song = newSong
                    self.gui.set_nnotes(newSong.nnotes)
                    self.gui.set_nchannels(newSong.curSection.nchannels)
                    self.player.sounds = []
                    for channel in self.song.curSection.channels:
                        self.player.addSound(channel.sound)
            case None:
                pass
            case _:
                self.running = False
                print(f"encountered unexpected event in controller.executeEvent(): {e}")
            
class Player(object):

    def __init__(self):
        self.sounds = []
    
    def addSound(self, soundPath):
        self.sounds += [pg.mixer.Sound(soundPath)]

    def playSounds(self, toPlayList):
        for i in toPlayList:
            pg.mixer.Sound.play(self.sounds[i])
