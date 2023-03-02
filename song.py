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

import pyaudio as pa


class Song(object):

    def __init__(self, name:str):
        self.name:str = name
        self.sections:[Section] = []
        self.tempo:int = 100
        self.nbeats:int = 8
        self.nbars:int = 2
        self.addSection()
        self.curSection = self.sections[0]
    
    def addSection(self, name:str=None):
        if not name: s = Section(str(len(self.sections)), self.nbeats*self.nbars)
        else : s = Section(name, self.nbeats*self.nbars)
        self.sections += [s]
    
class Section(object):

    def __init__(self, name:str, nnotes:int):
        self.nnotes = nnotes
        self.name:str = name
        self.channels:[Channel] = []
        kick = Sound("kick", "kick.wav")
        snare = Sound("snare", "snare.wav")
        self.addChannel(nnotes, kick)
        self.addChannel(nnotes, snare)

    def addChannel(self, nnotes:int, sound, name:str=None, ):
        if not name: c = Channel(sound.name, nnotes, sound)
        else: c = Channel(name, nnotes, sound)
        self.channels += [c]

class Sound(object):

    def __init__(self, name:str, path:str):
        self.name = name
        self.wav = path
    
    def play(self):
        pass

class Channel(object):

    def __init__(self, name:str, nnotes:int, sound:Sound):
        self.name:str = name
        self.sound:Sound = sound
        self.played:[bool] = [False for _ in range(nnotes)]
        self.volume:float = 0.5

