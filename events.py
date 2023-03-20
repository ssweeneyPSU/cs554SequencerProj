"""
events.py -- Sean Sweeney
classes to handle events in sound sequences project
"""

class Event(object):
    def __init__(self):
        pass

class ClickNoteEvent(Event):
    __match_args__ = ("chani", "notei")
    def __init__(self, chan_i, note_i):
        super().__init__()
        self.chani = chan_i
        self.notei = note_i

class ClickPlayEvent(Event):
    def __init__(self):
        super().__init__()

class ClickPauseEvent(Event):
    def __init__(self):
        super().__init__()

class AddChannelEvent(Event):
    def __init__(self):
        super().__init__()

class QuitEvent(Event):
    def __init__(self):
        super().__init__()