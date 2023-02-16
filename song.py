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


class Song(object):

    def __init__(self, name:str):
        self.name:str = name
        self.secs:[Section] = []
        self.tempo:int = 100
        self.nbeats:int = 8
        self.nbars:int = 2
    
    def addSection(self, name:str=None):
        if name: s = Section(str(len(self.secs)))
        else : s = Section(name)
        self.secs += [s]
    
class Section(object):

    def __init__(self, name:str, nnotes:int):
        self.nnotes = nnotes
        self.name:str = name
        self.channel:[Channel] = []

    def addChannel(self, name, nnotes, soud):
        pass

class Sound(object):

    def __init__(self, name:str):
        self.name = name

class Channel(object):

    def __init__(self, name:str, nnotes:int, sound:Sound):
        self.name:str = name
        self.sound:Sound = sound
        self.played:[bool] = [False for _ in range(nnotes)]
        self.volume:float = 0.5

