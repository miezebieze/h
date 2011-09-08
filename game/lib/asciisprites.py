""" Inspirated and partly taken from the game Gorillas.py by Al Sweigart.
    Visit him (and learn to make your own games) at:

        http://inventwithpython.com
"""
import pygame
from pygame.locals import SRCALPHA # Needed for transparency of background

class Image:
    def __init__(self, ascii, colours=None):
        self.ascii      = ascii
        self.colours    = colours or {'X': (255, 255, 255, 255)}
        self.update()

    def update(self):
        ''' Call this after You changed the ascii. '''
        self.asciilist  = self.ascii.split('\n')[1:-1]
        self.width      = max([len(x) for x in self.asciilist])
        self.height     = len(self.asciilist)
        self.surface    = pygame.Surface((self.width, self.height), SRCALPHA, 32)
        try: self.surface.fill(self.colours['bg'])
        except KeyError: self.surface.fill((0,0,0,0))
        self.update_colours()

    def update_colours(self):
        ''' Update all colours.
            Call this after You changed self.colours manually. '''
        for colour in self.colours:
            self.update_colour(colour)

    def update_colour(self, colour):
        ''' Update a single colour. '''
        if colour in self.colours:
            for y in range(self.height):
                for x in range(self.width):
                    if self.asciilist[y][x] == colour:
                        self.surface.set_at((x, y), self.colours[colour])
            print 'updated ' + colour
        
    def set_colour(self, key, value):
        ''' Set the colour of any byte in self.colours.'''
        self.colours[key] = value
        self.update_colour(key)

    def set_colours(self, colours, update=True):
        for i in colours:
            if colours[i] != self.colours[i]:
                self.set_colour(i, colours[i])#self.colours[i] = colours[i]
        if update:
            self.update_colours()

    def set_ascii(self, ascii):
        self.ascii = ascii
        self.update()

    def get_surface(self):
        return self.surface

class Animation:
    ''' Container class to show Image objects subsequently.

        self.frames are the indexes in self.timeline of self.images,
        which are the Image(object)s. '''
    def __init__(self, asciis, timeline=None, colours=None):
        self.frames   = []
        self.timeline = timeline or ['0']
        self.colours  = colours or {'X': (255, 255, 255, 255)}
        for i in range(len(asciis)):
            print i
            self.frames.append(Image(asciis[i], self.colours))

        self.curframe   = self.timeline[0]
        self.update_curframe()
        self.update_frames()

    def update_curframe(self):
        ''' Change surface to current frames'. '''
        self.curimage = self.frames[self.timeline[self.curframe]]
        self.surface = self.curimage.surface

    def update_frames(self):
        for i in range(len(self.frames)):
            self.frames[i].update()

    def set_colours(self, colours):
        for i in range(len(self.frames)):
            self.frames[i].set_colours(colours)

    def set_colour(self, key, value):
        for i in self.frames:
            self.frames[i].set_colour(key, value)

    def swap(self, amount = 1):
        if self.curframe + amount > len(self.timeline) -1:
            self.curframe = 0
        else:
            self.curframe += amount
        self.update_curframe()

    def get_image(self):
        frames = []
        for i in self.timeline:
            frames.append(self.frames[i])
        return frames

    def get_frames(self):
        images = []
        for i in self.timeline:
            images.append(self.frames[i].surface)
        return images

    def get_asciis(self):
        asciis = {}
        for i in self.frames:
            asciis[i] = self.frames[i].ascii
        return asciis

