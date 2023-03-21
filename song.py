"""
song.py -- Sean Sweeney
classes to represent a single song in sequencer
A song is the highest-level unit to work with and consists of one or more sections
    - tempo
    - number of beats (per measure)
    - number of bars (aka measure)
    - collection of sections
A section is a distinct seqeuncer "panel"
    - collection of channels
    - a name
    - number of notes per channel, to pass down
A channel is an instrument 
    - some sound to play
    - a measure*beats size bool array (play or don't play)
    - a name
    - volume
a sound is some sample to play and a name
    - the idea here is that I want to be able to generate sounds and also use samples that come from files
    - TODO: implement a sound
"""
import pygame as pg

verb:bool = True

class Song(object):

    def __init__(self, name:str):
        self.name:str = name
        self.sections:[Section] = []
        self.tempo:int = 100
        self.nbeats:int = 4
        self.nbars:int = 4
        self.nnotes = self.nbeats*self.nbars
        #self.player = pa.PyAudio()
        self.addSection()
        self.curSection = self.sections[0]
        self.play = False
    
    def addSection(self, name:str=None):
        if not name: s = Section(str(len(self.sections)), self.nbeats*self.nbars)
        else : s = Section(name, self.nbeats*self.nbars)
        self.sections += [s]

    def playNote(self, noteIndex):
        soundsToPlay = []
        for chan in self.curSection.channels:
            if chan.played[noteIndex]: 
                soundsToPlay += [chan.sound]
        for sound in soundsToPlay:
            sound.play()
    
class Section(object):

    def __init__(self, name:str, nnotes:int):
        self.nnotes = nnotes
        self.name:str = name
        self.channels:[Channel] = []
        self.nchannels = 0


    def addChannel(self, nnotes:int, sound:str, name:str=None, ):
        if not name: c = Channel(sound.name, nnotes, sound)
        else: c = Channel(name, nnotes, sound)
        self.channels += [c]
        self.nchannels += 1

class Channel(object):

    def __init__(self, name:str, nnotes:int, sound:str):
        self.name:str = name
        self.sound:str = sound
        self.played:[bool] = [False for _ in range(nnotes)]
        self.volume:float = 0.5

    def toggleNote(self, notei):
        if verb: print("toggled note")
        self.played[notei] = not self.played[notei]

