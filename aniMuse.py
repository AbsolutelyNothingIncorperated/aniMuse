##Simple music module, masking alsaseq and alsamidi into more usable parts
## esuM will be interface module

""" TODO:
Wrap the alsaseq module in a local object /?/

Better handling of channels
Sequences
non-note events
changing volume
"""


import alsaseq
import alsamidi

alsaseq.client("esuM", 1, 1, False) ##Placeholder until I get a channel fix working-  

chordModes = {#different chord structures. 
             #'name':(root,interval, interval... )
              'maj':(0,4,7),
              'min':(0,3,7),
              '5':(0,7),
              'tri':(0,6),
             }

class alsaclient(): #Alsaclient wrapper, will contain channels. VERY unclear as to the structure we want.
    def __init__(self, name, innum, outnum, queue):
        alsaseq.client(name, innum, outnum, queue)



class note:
    def __init__(self, channel, keynum, velocity):
        self.chan = channel
        self.key = keynum
        self.vel = velocity
        self.active = False

    def on(self, vel=None, chan=None):
        alsaseq.output(alsamidi.noteonevent(self.chan, self.key, self.vel))
        self.active = True
 
    def off(self):
        alsaseq.output(alsamidi.noteoffevent(self.chan, self.key, self.vel))
        self.active = False

    def tog(self):
        if self.active:
            self.off()
        else:
            self.on()

    def __add__(self, b):
        #note plus note equals chord
        if hasattr(b, 'notes'):
            notes = b.notes + [self]
            return chord(notes)
        else:
            return chord([self, b])

def chordFromMode(channel, keynum, velocity, mode):
    notes = []
    for mod in chordModes[mode]:
        key = keynum + mod
        notes.append(note(channel, key, velocity))
    return chord(notes)

class chord():
    #could rewrite this by subclassing lists, or dicts. but YAGNI. also too lazy.
    def __init__(self, notes):
        self.notes = notes
        self.active = False

    def on(self, vel=None, chan=None):
        for note in self.notes:
            if vel:
                note.vel = vel
            note.on()
        self.active = True
 
    def off(self):
        for note in self.notes:
            note.off()
        self.active = False

    def tog(self):
        for note in self.notes:
            note.tog()
        if self.active:
            self.active = False
        else:
            self.active = True

    def __add__(self, b):
        if hasattr(b, 'notes'):
            notes = b.notes + self.notes
            return chord(notes)
        else:
            notes = self.notes + [b]
            return chord(notes)

class sequence():
    def __init__(self):
        self.notes = ()
        self.time = 0


__doc__ = """

>>> import aniMuse

Create a note (through channel 0, key number 60, at a velocity of 144)
>>> A = aniMuse.note(0,60,144)

Trigger it to play
>>> A.on()

And to stop playing
>>> A.off()

Add another note for good measure,
>>> B = aniMuse.note(0,65,144)
>>> B.on()
>>> B.off()

and add them to get a chord.
>>> Chord1 = A + B
>>> Chord1.on()
>>> Chord1.off()

Add another note to that chord
>>> C = aniMuse.note(0,70,144)
>>> Chord2 = C + Chord1
>>> Chord2.on()
>>> Chord2.off()

Alternatively, create chords manually:
>>> Chord3 = chord([A,B,C])
>>> Chord3.on()
>>> Chord3.off()

Or from a modal constructor (takes same arguements as a note, plus the mode type [major, in this case]):
>>> Chord4 = chordFromMode(0,50,144,'maj')
>>> Chord4.on()
>>> Chord4.off()

Add chords to get more chords:
>>> Chord5 = Chord1 + Chord4
>>> Chord5.on()
>>> Chord5.off()

"""
