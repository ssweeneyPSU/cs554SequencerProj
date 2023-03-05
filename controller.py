"""
controller.py -- Sean Sweeney
Controler class exectutes event based changes on interfaces and songs
"""

class Controller(object):

    def __init__(self, song, gui, handler):
        self.song = song
        self.gui = gui
        self.handler = handler
    
    def run(self):
        